from __future__ import print_function

import argparse
import json

import numpy as np

from dataset_pre_processing.metadata import create_metadata, create_one_type_dictionary
from dataset_pre_processing.scaling import scale_and_save_scaler


VARIABLES = [
    "n1_radius",
    "n1_texture",
    "n1_perimeter",
    "n1_area",
    "n1_smoothness",
    "n1_compactness",
    "n1_concavity",
    "n1_concave_points",
    "n1_symmetry",
    "n1_fractal_dimension",
    "n2_radius",
    "n2_texture",
    "n2_perimeter",
    "n2_area",
    "n2_smoothness",
    "n2_compactness",
    "n2_concavity",
    "n2_concave_points",
    "n2_symmetry",
    "n2_fractal_dimension",
    "n3_radius",
    "n3_texture",
    "n3_perimeter",
    "n3_area",
    "n3_smoothness",
    "n3_compactness",
    "n3_concavity",
    "n3_concave_points",
    "n3_symmetry",
    "n3_fractal_dimension",
]

NUM_SAMPLES = [
    357,  # 0 = negative = B = benign
    212,  # 1 = positive = M = malignant
]

CLASSES = [
    "benign",
    "malignant",
]

CLASS_TO_INDEX = {
    "B": 0,
    "M": 1,
}


def breast_transform(input_path, features_path, labels_path, metadata_path, scaler_path):
    metadata = create_metadata(VARIABLES,
                               create_one_type_dictionary("numerical", VARIABLES),
                               {},
                               sum(NUM_SAMPLES),
                               CLASSES)

    input_file = open(input_path, "r")

    features = np.zeros((metadata["num_samples"], metadata["num_features"]), dtype=np.float32)
    labels = np.zeros(metadata["num_samples"], dtype=np.int32)

    # transform
    i = 0
    line = input_file.readline()
    while line != "":
        line = line.rstrip("\n")
        values = line.split(",")

        # the amount of values (minus the ID and the label)
        # should be the same as the amount of variables
        assert len(values) - 2 == len(VARIABLES), str((len(values), len(VARIABLES)))

        # assign each column with the right mapping
        # (skip the ID and the label)
        for variable, value in zip(VARIABLES, values[2:]):
            value = float(value)
            features[i, metadata["value_to_index"][variable]] = value

        # the second value is the label
        labels[i] = CLASS_TO_INDEX[values[1]]

        # next row
        i += 1
        line = input_file.readline()

    # scale
    if scaler_path is not None:
        features = scale_and_save_scaler(features, scaler_path)

    assert i == metadata["num_samples"]

    num_positive_samples = int(labels.sum())
    num_negative_samples = labels.shape[0] - num_positive_samples

    assert num_negative_samples == NUM_SAMPLES[0]
    assert num_positive_samples == NUM_SAMPLES[1]

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

    breast_transform(options.input,
                     options.features,
                     options.labels,
                     options.metadata,
                     options.scaler)


if __name__ == "__main__":
    main()
