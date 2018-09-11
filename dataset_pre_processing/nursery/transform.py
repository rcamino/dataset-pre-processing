from __future__ import print_function

import argparse
import json

import numpy as np
import pandas as pd

from scipy.sparse import csr_matrix, save_npz

from dataset_pre_processing.metadata import create_metadata, create_class_to_index, create_one_type_dictionary


VARIABLES = [
    "parents",
    "has_nurs",
    "form",
    "children",
    "housing",
    "finance",
    "social",
    "health",
    "class",
]

CLASSES = [
    "not_recom",
    "recommend",
    "very_recom",
    "priority",
    "spec_prior"
]

CLASS_TO_INDEX = create_class_to_index(CLASSES)


def nursery_transform(input_path, features_path, labels_path, metadata_path):
    df = pd.read_csv(input_path, names=VARIABLES)

    variables = sorted(df.columns)
    variables.remove("class")

    categorical_values = {}
    for variable in variables:
        categorical_values[variable] = df[variable].unique()

    num_samples = len(df)

    metadata = create_metadata(VARIABLES,
                               create_one_type_dictionary("categorical", VARIABLES),
                               categorical_values,
                               num_samples,
                               CLASSES)

    with open(metadata_path, "w") as metadata_file:
        json.dump(metadata, metadata_file)

    ones = []
    rows = []
    cols = []

    labels = np.zeros(num_samples, dtype=np.int32)

    for row_number, (_, row) in enumerate(df.iterrows()):
        labels[row_number] = CLASS_TO_INDEX[row["class"]]

        for variable in variables:
            value = row[variable]
            feature_number = metadata["value_to_index"][variable][value]

            ones.append(1)
            rows.append(row_number)
            cols.append(feature_number)

    output = csr_matrix((ones, (rows, cols)), shape=(num_samples, metadata["num_features"]), dtype=np.uint8)

    save_npz(features_path, output)
    np.save(labels_path, labels)


def main():
    options_parser = argparse.ArgumentParser(
        description="Transform the Nursery data into a feature matrix and label array."
                    + " Dataset: https://archive.ics.uci.edu/ml/datasets/Nursery."
    )

    options_parser.add_argument("input", type=str, help="Input Nursery data in text format.")
    options_parser.add_argument("features", type=str, help="Output features in numpy array format.")
    options_parser.add_argument("labels", type=str, help="Output labels in numpy array format.")
    options_parser.add_argument("metadata", type=str, help="Metadata in json format.")

    options = options_parser.parse_args()

    nursery_transform(options.input, options.features, options.labels, options.metadata)


if __name__ == "__main__":
    main()
