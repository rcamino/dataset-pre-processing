import argparse
import json

import numpy as np

from dataset_pre_processing.metadata import create_metadata, create_one_type_dictionary, update_feature_distributions, \
    update_class_distribution, validate_class_distribution, validate_num_samples
from dataset_pre_processing.scaling import scale_and_save_scaler


VARIABLES = [
    "Clump Thickness",
    "Uniformity of Cell Size",
    "Uniformity of Cell Shape",
    "Marginal Adhesion",
    "Single Epithelial Cell Size",
    "Bare Nuclei",
    "Bland Chromatin",
    "Normal Nucleoli",
    "Mitoses",
]

NUM_SAMPLES = {
    True: [
        444,  # 0 = negative = 2 = benign
        239,  # 1 = positive = 4 = malignant
    ],
    False: [
        458,  # 0 = negative = 2 = benign
        241,  # 1 = positive = 4 = malignant
    ]
}

CLASSES = [
    "benign",
    "malignant",
]

CLASS_TO_INDEX = {
    "2": 0,
    "4": 1,
}


def transform(input_path, features_path, labels_path, metadata_path, ignore_missing, scaler_path):
    metadata = create_metadata(VARIABLES,
                               create_one_type_dictionary("numerical", VARIABLES),
                               {},
                               sum(NUM_SAMPLES[ignore_missing]),
                               CLASSES)

    input_file = open(input_path, "r")

    # initialize outputs
    features = np.zeros((metadata["num_samples"], metadata["num_features"]), dtype=np.float32)
    labels = np.zeros(metadata["num_samples"], dtype=np.int32)

    # transform
    sample_index = 0
    line = input_file.readline()
    while line != "":
        line = line.rstrip("\n")
        values = line.split(",")

        missing_values = False
        for value in values:
            if value == "?" or value == "":
                missing_values = True
                break

        # if there are missing values the ignore missing flag is set then ignore the row
        if not missing_values or not ignore_missing:
            # the amount of values (minus the ID and the label)
            # should be the same as the amount of variables
            assert len(values) - 2 == len(VARIABLES), str((len(values), len(VARIABLES)))

            # assign each column with the right mapping
            # (skip the ID and the label)
            for variable, value in zip(VARIABLES, values[1:-1]):
                if value == "?" or value == "":
                    value = np.nan
                else:
                    value = float(value)
                features[sample_index, metadata["value_to_index"][variable]] = value

            # the second value is the label
            labels[sample_index] = CLASS_TO_INDEX[values[-1]]

            # next row
            sample_index += 1

        # next line
        line = input_file.readline()

    # scale
    if scaler_path is not None:
        features = scale_and_save_scaler(features, scaler_path)

    # add distributions to the metadata
    update_feature_distributions(metadata, features)
    update_class_distribution(metadata, labels)

    # validate the known distributions
    validate_num_samples(metadata, sample_index)
    validate_class_distribution(metadata, NUM_SAMPLES[ignore_missing])

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

    options_parser.add_argument("--ignore_missing", action="store_true", help="Ignore rows with missing values.")

    options_parser.add_argument("--scaler", type=str,
                                help="Output scikit-learn MinMaxScaler in pickle format. Enables scaling to (0, 1).")

    options = options_parser.parse_args(args=args)

    transform(options.input, options.features, options.labels, options.metadata, options.ignore_missing, options.scaler)


if __name__ == "__main__":
    main()
