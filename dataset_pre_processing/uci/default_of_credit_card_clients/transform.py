from __future__ import print_function

import argparse
import csv
import json

import numpy as np

from dataset_pre_processing.metadata import create_metadata
from dataset_pre_processing.scaling import scale_and_save_scaler


NUM_SAMPLES = 30000

TYPES = {
    "LIMIT_BAL": "numerical",
    "SEX": "categorical",
    "EDUCATION": "categorical",
    "MARRIAGE": "categorical",
    "AGE": "numerical",
    "PAY_0": "categorical",
    "PAY_2": "categorical",
    "PAY_3": "categorical",
    "PAY_4": "categorical",
    "PAY_5": "categorical",
    "PAY_6": "categorical",
    "BILL_AMT1": "numerical",
    "BILL_AMT2": "numerical",
    "BILL_AMT3": "numerical",
    "BILL_AMT4": "numerical",
    "BILL_AMT5": "numerical",
    "BILL_AMT6": "numerical",
    "PAY_AMT1": "numerical",
    "PAY_AMT2": "numerical",
    "PAY_AMT3": "numerical",
    "PAY_AMT4": "numerical",
    "PAY_AMT5": "numerical",
    "PAY_AMT6": "numerical",
}

REPAYMENT_STATUS_VALUES = [
    "no consumption",
    "paid in full",
    "use of revolving credit",
    "payment delay for one month",
    "payment delay for one month",
    "payment delay for two months",
    "payment delay for three months",
    "payment delay for four months",
    "payment delay for five months",
    "payment delay for six months",
    "payment delay for eight months",
    "payment delay for nine months and above",
]

VALUES = {
    "SEX": ["male", "female"],
    # all the "others" will get merged
    "EDUCATION": ["others", "graduate school", "university", "high school", "others", "others", "others"],
    "MARRIAGE": ["others", "married", "single", "divorce"],
    "PAY_0": REPAYMENT_STATUS_VALUES,
    "PAY_2": REPAYMENT_STATUS_VALUES,
    "PAY_3": REPAYMENT_STATUS_VALUES,
    "PAY_4": REPAYMENT_STATUS_VALUES,
    "PAY_5": REPAYMENT_STATUS_VALUES,
    "PAY_6": REPAYMENT_STATUS_VALUES,
}


def create_original_to_value_map(variable, first_inclusive, last_inclusive):
    return dict([(i, VALUES[variable][i - first_inclusive])
                 for i in range(first_inclusive, last_inclusive + 1)])


ORIGINAL_ENCODING_TO_VALUES = {
    "SEX": create_original_to_value_map("SEX", 1, 2),
    "EDUCATION": create_original_to_value_map("EDUCATION", 0, 6),
    "MARRIAGE": create_original_to_value_map("MARRIAGE", 0, 3),
    "PAY_0": create_original_to_value_map("PAY_0", -2, 9),
    "PAY_2": create_original_to_value_map("PAY_2", -2, 9),
    "PAY_3": create_original_to_value_map("PAY_3", -2, 9),
    "PAY_4": create_original_to_value_map("PAY_4", -2, 9),
    "PAY_5": create_original_to_value_map("PAY_5", -2, 9),
    "PAY_6": create_original_to_value_map("PAY_6", -2, 9),
}

CLASSES = [
    "no default payment next month",
    "default payment next month",
]


def default_credit_card_transform(input_path, features_path, labels_path, metadata_path, scaler_path):
    input_file = open(input_path, "r")
    reader = csv.DictReader(input_file)

    variables = set(reader.fieldnames)
    variables.remove("ID")
    variables.remove("default payment next month")

    metadata = create_metadata(variables, TYPES, VALUES, NUM_SAMPLES, CLASSES)

    features = np.zeros((metadata["num_samples"], metadata["num_features"]), dtype=np.float32)
    labels = np.zeros(metadata["num_samples"], dtype=np.int32)

    # transform
    for i, row in enumerate(reader):
        for j, variable in enumerate(metadata["variables"]):
            value = row[variable]
            if TYPES[variable] == "numerical":
                value = float(value)
                features[i, metadata["value_to_index"][variable]] = value
            elif TYPES[variable] == "categorical":
                value = int(float(value))
                assert value in ORIGINAL_ENCODING_TO_VALUES[variable], \
                    "'{}' is not a valid value for '{}'".format(value, variable)
                value = ORIGINAL_ENCODING_TO_VALUES[variable][value]
                features[i, metadata["value_to_index"][variable][value]] = 1.0

        # the class needs to be transformed
        labels[i] = int(row["default payment next month"].replace(".0", ""))

    # scale
    if scaler_path is not None:
        features = scale_and_save_scaler(features, scaler_path)

    assert i == metadata["num_samples"] - 1

    np.save(features_path, features)
    np.save(labels_path, labels)

    input_file.close()

    with open(metadata_path, "w") as metadata_file:
        json.dump(metadata, metadata_file)


def main(args=None):
    options_parser = argparse.ArgumentParser(description="Transform the data into a feature matrix and label array.")

    options_parser.add_argument("input", type=str, help="Input data in text format.")
    options_parser.add_argument("features", type=str, help="Output features in numpy array format.")
    options_parser.add_argument("labels", type=str, help="Output labels in numpy array format.")
    options_parser.add_argument("metadata", type=str, help="Metadata in json format.")

    options_parser.add_argument("--scaler", type=str,
                                help="Output scikit-learn MinMaxScaler in pickle format. Enables scaling to (0, 1).")

    options = options_parser.parse_args(args=args)

    default_credit_card_transform(options.input,
                                  options.features,
                                  options.labels,
                                  options.metadata,
                                  options.scaler)


if __name__ == "__main__":
    main()
