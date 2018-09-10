from __future__ import print_function

import argparse
import json
import re

from datetime import datetime

import numpy as np

from sklearn.preprocessing.data import MinMaxScaler


ORIGINAL_VARIABLES = [
    "Date flow start",
    "Durat",
    "Prot",
    "Src IP Addr:Port",
    "Dst IP Addr:Port",
    "Flags",
    "Tos",
    "Packets Bytes",
    "Flows",
    "Label",
    "Labels",
]

NEW_VARIABLES = [
    "Time flow start",
    "Durat",
    "Prot",
    # "Src IP Addr",
    # "Src IP Port",
    # "Dst IP Addr",
    # "Dst IP Port",
    "Flags",
    "Tos",
    "Packets Bytes",
    "Flows",
    # "Label",
    "Labels",
]

TYPES = {
    "Time flow start": "numerical",
    "Durat": "numerical",
    "Prot": "categorical",
    # "Src IP Addr": "categorical",
    # "Src IP Port": "categorical",
    # "Dst IP Addr": "categorical",
    # "Dst IP Port": "categorical",
    "Flags": "categorical",
    "Tos": "categorical",
    "Packets Bytes": "numerical",
    "Flows": "numerical",
    # "Label": "categorical",
    "Labels": "categorical",
}

ARROW_REGEX = re.compile(r"[\t ]+->[\t ]+")
MULTI_TAB_REGEX = re.compile(r"\t\t+")
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def parse_row(line):
    tmp_line = MULTI_TAB_REGEX.sub("\t", line)
    tmp_line = ARROW_REGEX.sub("\t", tmp_line)
    tokens = tmp_line.strip().split("\t")
    flags = True
    if len(tokens) != len(ORIGINAL_VARIABLES):
        if len(tokens) == len(ORIGINAL_VARIABLES) - 1:
            print("Assuming no Flags: {}.".format(tokens))
            flags = False
        else:
            raise Exception("Invalid line: '{}'.".format(line))
    j = 0
    row = {}
    for variable in ORIGINAL_VARIABLES:
        if variable == "Date flow start":
            row["Date flow start"] = datetime.strptime(tokens[j][:-4], DATE_FORMAT)  # ignore millis
            j += 1
        elif variable in ["Src IP Addr:Port", "Dst IP Addr:Port"]:
            address_port = tokens[j].split(":")
            if len(address_port) == 2:
                address, port = address_port
            elif len(address_port) > 2 or len(address_port) == 1:
                address = tokens[j]
                port = ""
            else:
                raise Exception("Invalid address and port: '{}'.".format(tokens[j]))

            if variable == "Src IP Addr:Port":
                row["Src IP Addr"] = address
                row["Src IP Port"] = port
            else:
                row["Dst IP Addr"] = address
                row["Dst IP Port"] = port
            j += 1
        elif variable == "Flags":
            if flags:
                row["Flags"] = tokens[j]
                j += 1
            else:
                row["Flags"] = ""
        else:
            row[variable] = tokens[j]
            j += 1

    return row


def create_metadata(input_file):
    numerical_variables = []
    categorical_variables = []
    for variable in NEW_VARIABLES:
        variable_type = TYPES[variable]
        if variable_type == "numerical":
            numerical_variables.append(variable)
        if variable_type == "categorical":
            categorical_variables.append(variable)

    categorical_variables = sorted(categorical_variables)
    numerical_variables = sorted(numerical_variables)

    feature_number = 0
    value_to_index = {}
    index_to_value = []
    variable_sizes = []
    variable_types = []

    values = {}
    for variable in categorical_variables:
        values[variable] = set()

    num_samples = 0
    start_time = None

    line = input_file.readline().strip()
    while line != "":
        row = parse_row(line)
        if start_time is None or row["Date flow start"] < start_time:
            start_time = row["Date flow start"]

        for variable in NEW_VARIABLES:
            if TYPES[variable] == "categorical":
                values[variable].add(row[variable])
        num_samples += 1
        line = input_file.readline().strip()

    for variable in categorical_variables:
        variable_types.append("categorical")
        variable_values = sorted(values[variable])
        variable_sizes.append(len(variable_values))
        value_to_index[variable] = {}
        for value in variable_values:
            index_to_value.append((variable, value))
            value_to_index[variable][value] = feature_number
            feature_number += 1

    for variable in numerical_variables:
        variable_types.append("numerical")
        variable_sizes.append(1)
        value_to_index[variable] = feature_number
        feature_number += 1

    num_features = feature_number

    return {
        "variables": categorical_variables + numerical_variables,
        "variable_sizes": variable_sizes,
        "variable_types": variable_types,
        "index_to_value": index_to_value,
        "value_to_index": value_to_index,
        "num_features": num_features,
        "num_samples": num_samples,
        "start_time": start_time.strftime(DATE_FORMAT)
    }


def read_binary(value):
    return int(float(value.strip()))


def netflow_transform(input_path, features_path, labels_path, metadata_path):
    input_file = open(input_path, "r")
    input_file.readline()  # ignore malformed header

    metadata = create_metadata(input_file)

    input_file.seek(0)  # start again
    input_file.readline()  # ignore malformed header

    start_time = datetime.strptime(metadata["start_time"], DATE_FORMAT)

    features = np.zeros((metadata["num_samples"], metadata["num_features"]), dtype=np.float32)
    labels = np.zeros(metadata["num_samples"], dtype=np.float32)

    # transform
    i = 0
    line = input_file.readline().strip()
    while line != "":
        row = parse_row(line)

        for variable in NEW_VARIABLES:
            if TYPES[variable] == "numerical":
                if variable == "Time flow start":
                    value = (row["Date flow start"] - start_time).total_seconds()
                else:
                    value = float(row[variable])
                features[i, metadata["value_to_index"][variable]] = value
            elif TYPES[variable] == "categorical":
                features[i, metadata["value_to_index"][variable][row[variable]]] = 1.0

        i += 1
        line = input_file.readline().strip()

    # scale
    scaler = MinMaxScaler(feature_range=(0, 1), copy=False)
    scaler.fit_transform(features)

    assert i == metadata["num_samples"], "Expected {:d} samples but got {:d}.".format(metadata["num_samples"], i)

    print("Total samples: ", features.shape[0])
    print("Features: ", features.shape[1])

    np.save(features_path, features)
    np.save(labels_path, labels)

    input_file.close()

    metadata["features_min"] = scaler.data_min_.tolist()
    metadata["features_max"] = scaler.data_max_.tolist()

    with open(metadata_path, "w") as metadata_file:
        json.dump(metadata, metadata_file)


def main(args=None):
    options_parser = argparse.ArgumentParser(description="Transform the Netflow data into feature matrices.")

    options_parser.add_argument("input", type=str, help="Input Netflow data in text format.")
    options_parser.add_argument("features", type=str, help="Output features in numpy array format.")
    options_parser.add_argument("labels", type=str, help="Output labels in numpy array format.")
    options_parser.add_argument("metadata", type=str, help="Metadata in json format.")

    options = options_parser.parse_args(args=args)

    netflow_transform(options.input, options.features, options.labels, options.metadata)


if __name__ == "__main__":
    main()