from __future__ import print_function

import argparse
import csv
import json
import os

import numpy as np

from scipy.sparse import csr_matrix, save_npz


MODES = ["train", "test"]


def ipinyou_transform(directory):
    campaigns = sorted([subdirectory for subdirectory in os.listdir(directory) if subdirectory != "all"])

    for campaign in campaigns:
        print("Campaign:", campaign)
        ipinyou_transform_campaign(directory, campaign)


def ipinyou_transform_campaign(directory, campaign):
        print("Extracting metadata...")

        metadata = ipinyou_extract_metadata(directory, campaign)

        with open(os.path.join(directory, str(campaign), "metadata.js"), "w") as metadata_file:
            json.dump(metadata, metadata_file)

        for mode in MODES:
            print("Transforming mode:", mode)
            ipinyou_transform_campaign_mode(directory, campaign, mode, metadata)


def ipinyou_extract_metadata(directory, campaign):
    values_by_variable = None
    variables = None

    for mode in MODES:
        input_path = os.path.join(directory, str(campaign), "{}-filtered.log.txt".format(mode))
        input_file = open(input_path, "r")
        reader = csv.DictReader(input_file, delimiter="\t")

        if values_by_variable is None or variables is None:
            variables = set(reader.fieldnames)
            variables.remove("click")
            variables.remove("payprice")
            variables = sorted(variables)

            values_by_variable = {}

            for variable in variables:
                values_by_variable[variable] = set()

        print("Extracting metadata from mode:", mode)
        for row in reader:
            for variable in variables:
                variable_value = row[variable]
                values_by_variable[variable].add(variable_value)

        input_file.close()

    variable_sizes = []
    index_to_value = []
    value_to_index = {}
    feature_index = 0
    for variable in variables:
        variable_values = sorted(values_by_variable[variable])
        variable_sizes.append(len(variable_values))
        value_to_index[variable] = {}
        for variable_value in variable_values:
            value_to_index[variable][variable_value] = feature_index
            index_to_value.append((variable, variable_value))
            feature_index += 1

    metadata = {
        "variables": variables,
        "variable_sizes": variable_sizes,
        "index_to_value": index_to_value,
        "value_to_index": value_to_index,
        "num_features": feature_index
    }

    return metadata


def ipinyou_transform_campaign_mode(directory, campaign, mode, metadata):
    input_file_path = os.path.join(directory, str(campaign), "{}-filtered.log.txt".format(mode))
    features_file_path = os.path.join(directory, str(campaign), "{}-filtered.features.npz".format(mode))
    click_file_path = os.path.join(directory, str(campaign), "{}-filtered.click.npy".format(mode))
    price_file_path = os.path.join(directory, str(campaign), "{}-filtered.price.npy".format(mode))

    input_file = open(input_file_path, "r")
    reader = csv.DictReader(input_file, delimiter="\t")

    ones = []
    rows = []
    cols = []
    click = []
    price = []

    num_samples = 0
    for i, row in enumerate(reader):
        feature_indices = []
        click.append(int(row["click"]))
        price.append(float(row["payprice"]))

        for variable in metadata["variables"]:
            variable_value = row[variable]
            feature_index = metadata["value_to_index"][variable][variable_value]
            feature_indices.append(feature_index)

        for j in sorted(feature_indices):
            ones.append(1)
            rows.append(i)
            cols.append(j)

        num_samples += 1

    input_file.close()

    features = csr_matrix((ones, (rows, cols)), shape=(num_samples, metadata["num_features"]), dtype=np.uint8)

    save_npz(features_file_path, features)
    np.save(click_file_path, click)
    np.save(price_file_path, price)


def main():
    options_parser = argparse.ArgumentParser(
        description="Transform iPinYou train and test text data into numpy arrays."
                    + " Dataset: http://data.computational-advertising.org"
    )

    options_parser.add_argument(
        "directory",
        type=str,
        help="iPinYou data directory containing train-filtered.log.txt and test-filtered.log.txt"
    )

    options = options_parser.parse_args()

    ipinyou_transform(options.directory)


if __name__ == "__main__":
    main()
