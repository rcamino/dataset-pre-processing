from __future__ import print_function

import argparse
import json

import numpy as np

from dataset_pre_processing.metadata import create_metadata, create_one_type_dictionary, update_feature_distributions, \
    update_class_distribution, validate_num_samples, validate_class_distribution
from dataset_pre_processing.scaling import scale_and_save_scaler


VARIABLES = [
    "word_freq_make",
    "word_freq_address",
    "word_freq_all",
    "word_freq_3d",
    "word_freq_our",
    "word_freq_over",
    "word_freq_remove",
    "word_freq_internet",
    "word_freq_order",
    "word_freq_mail",
    "word_freq_receive",
    "word_freq_will",
    "word_freq_people",
    "word_freq_report",
    "word_freq_addresses",
    "word_freq_free",
    "word_freq_business",
    "word_freq_email",
    "word_freq_you",
    "word_freq_credit",
    "word_freq_your",
    "word_freq_font",
    "word_freq_000",
    "word_freq_money",
    "word_freq_hp",
    "word_freq_hpl",
    "word_freq_george",
    "word_freq_650",
    "word_freq_lab",
    "word_freq_labs",
    "word_freq_telnet",
    "word_freq_857",
    "word_freq_data",
    "word_freq_415",
    "word_freq_85",
    "word_freq_technology",
    "word_freq_1999",
    "word_freq_parts",
    "word_freq_pm",
    "word_freq_direct",
    "word_freq_cs",
    "word_freq_meeting",
    "word_freq_original",
    "word_freq_project",
    "word_freq_re",
    "word_freq_edu",
    "word_freq_table",
    "word_freq_conference",
    "char_freq_;",
    "char_freq_(",
    "char_freq_[",
    "char_freq_!",
    "char_freq_$",
    "char_freq_#",
    "capital_run_length_average",
    "capital_run_length_longest",
    "capital_run_length_total",
]

NUM_SAMPLES = [
    2788,  # 0 = negative = not-spam
    1813,  # 1 = positive = spam
]

CLASSES = [
    "not-spam",
    "spam"
]


def spambase_transform(input_path, features_path, labels_path, metadata_path, scaler_path):
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

        # the amount of values (minus the label)
        # should be the same as the amount of variables
        assert len(values) - 1 == len(VARIABLES), str((len(values) - 1, len(VARIABLES)))

        # assign each column with the right mapping
        for variable, value in zip(VARIABLES, values[:-1]):
            value = float(value)
            features[i, metadata["value_to_index"][variable]] = value

        # the last value is the label
        labels[i] = int(values[-1])

        # next row
        i += 1
        line = input_file.readline()

    # scale
    if scaler_path is not None:
        features = scale_and_save_scaler(features, scaler_path)

    # add distributions to the metadata
    update_feature_distributions(metadata, features)
    update_class_distribution(metadata, labels)

    # validate the known distributions
    validate_num_samples(metadata, i)
    validate_class_distribution(metadata, NUM_SAMPLES)

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

    spambase_transform(options.input,
                       options.features,
                       options.labels,
                       options.metadata,
                       options.scaler)


if __name__ == "__main__":
    main()
