from __future__ import print_function

import argparse
import csv
import json

import numpy as np

from scipy.sparse import csr_matrix, save_npz

from dataset_pre_processing.metadata import create_metadata, create_one_type_dictionary


def uscensus_transform(input_path, output_path, metadata_path):
    input_file = open(input_path, "r")
    reader = csv.DictReader(input_file)

    variables = sorted(reader.fieldnames)
    variables.remove("caseid")

    categorical_values = {}
    for variable in variables:
        categorical_values[variable] = set()

    print("Counting values...")
    for row_number, row in enumerate(reader):
        if row_number % 10000 == 0:
            print("{:d} rows read".format(row_number))

        for variable in variables:
            value = row[variable]
            categorical_values[variable].add(value)

    print("Saving metadata...")

    num_samples = row_number + 1

    metadata = create_metadata(variables,
                               create_one_type_dictionary("categorical", variables),
                               categorical_values,
                               num_samples)

    with open(metadata_path, "w") as metadata_file:
        json.dump(metadata, metadata_file)

    input_file.seek(0)

    ones = []
    rows = []
    cols = []

    print("Writing...")

    for row_number, row in enumerate(reader):
        if row_number % 10000 == 0:
            print("{:d} rows read".format(row_number))

        for variable in variables:
            value = row[variable]
            feature_number = metadata["value_to_index"][variable][value]

            ones.append(1)
            rows.append(row_number)
            cols.append(feature_number)

    output = csr_matrix((ones, (rows, cols)), shape=(num_samples, metadata["num_features"]), dtype=np.uint8)

    save_npz(output_path, output)

    print("Done.")

    input_file.close()


def main(args=None):
    options_parser = argparse.ArgumentParser(
        description="Transform the US Census Data (1990) text data into feature matrix."
                    + " Dataset: https://archive.ics.uci.edu/ml/datasets/US+Census+Data+(1990)."
    )

    options_parser.add_argument("input", type=str, help="Input USCensus data in text format.")
    options_parser.add_argument("output", type=str, help="Output features in sparse scipy matrix format.")
    options_parser.add_argument("metadata", type=str, help="Metadata in json format.")

    options = options_parser.parse_args(args=args)

    uscensus_transform(options.input, options.output, options.metadata)


if __name__ == "__main__":
    main()
