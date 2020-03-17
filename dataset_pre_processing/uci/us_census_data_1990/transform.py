from __future__ import print_function

import argparse
import csv
import json

import numpy as np

from scipy.sparse import csr_matrix, save_npz

from dataset_pre_processing.metadata import create_metadata, create_one_type_dictionary


NUM_SAMPLES = 2458285


def uscensus_transform(input_path, output_path, metadata_path):
    input_file = open(input_path, "r")
    reader = csv.DictReader(input_file)

    # read the variables from the header
    variables = sorted(reader.fieldnames)
    # but ignore the ID
    variables.remove("caseid")

    # first read everything to count the values per variable
    categorical_values = {}
    for variable in variables:
        categorical_values[variable] = set()

    for row_number, row in enumerate(reader):
        for variable in variables:
            value = row[variable]
            categorical_values[variable].add(value)

    # now create the metadata
    metadata = create_metadata(variables,
                               create_one_type_dictionary("categorical", variables),
                               categorical_values,
                               NUM_SAMPLES)

    # go back to the beginning
    input_file.seek(0)
    # the reader needs to be re-initialized
    # using tell after reading the headers does not work during the reader iteration
    reader = csv.DictReader(input_file)

    # now fill the feature matrix with the right encoding
    ones = []
    rows = []
    cols = []

    for row_number, row in enumerate(reader):
        for variable in variables:
            value = row[variable]
            feature_number = metadata["value_to_index"][variable][value]

            ones.append(1)
            rows.append(row_number)
            cols.append(feature_number)

    output = csr_matrix((ones, (rows, cols)), shape=(metadata["num_samples"], metadata["num_features"]), dtype=np.uint8)

    save_npz(output_path, output)

    input_file.close()

    with open(metadata_path, "w") as metadata_file:
        json.dump(metadata, metadata_file)


def main(args=None):
    options_parser = argparse.ArgumentParser(description="Transform the data into a feature matrix.")

    options_parser.add_argument("input", type=str, help="Input data in text format.")
    options_parser.add_argument("output", type=str, help="Output features in csr matrix compressed format.")
    options_parser.add_argument("metadata", type=str, help="Metadata in json format.")

    options = options_parser.parse_args(args=args)

    uscensus_transform(options.input, options.output, options.metadata)


if __name__ == "__main__":
    main()
