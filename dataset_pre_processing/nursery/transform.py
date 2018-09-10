from __future__ import print_function

import argparse
import json

import numpy as np
import pandas as pd

from scipy.sparse import csr_matrix, save_npz


FIELDS = [
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

CLASS_TO_INDEX = dict([(c, i) for i, c in enumerate(CLASSES)])


def nursery_transform(input_path, features_path, labels_path, metadata_path):
    df = pd.read_csv(input_path, names=FIELDS)

    variables = sorted(df.columns)
    variables.remove("class")

    values_by_variable = {}
    for variable in variables:
        values_by_variable[variable] = df[variable].unique()

    feature_number = 0
    index_to_value = []
    value_to_index = {}
    variable_sizes = []
    variable_types = []

    for variable in variables:
        variable_types.append("categorical")
        values = sorted(values_by_variable[variable])
        variable_sizes.append(len(values))
        value_to_index[variable] = {}
        for value in values:
            index_to_value.append((variable, value))
            value_to_index[variable][value] = feature_number
            feature_number += 1

    num_samples = len(df)
    num_features = feature_number

    metadata = {
        "variables": variables,
        "variable_sizes": variable_sizes,
        "variable_types": variable_types,
        "index_to_value": index_to_value,
        "value_to_index": value_to_index,
        "num_features": num_features,
        "num_samples": num_samples,
        "classes": CLASSES
    }

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
            feature_number = value_to_index[variable][value]

            ones.append(1)
            rows.append(row_number)
            cols.append(feature_number)

    output = csr_matrix((ones, (rows, cols)), shape=(num_samples, num_features), dtype=np.uint8)

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
