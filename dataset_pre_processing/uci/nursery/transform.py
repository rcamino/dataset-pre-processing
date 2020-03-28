import argparse
import csv
import json

import numpy as np

from dataset_pre_processing.metadata import create_metadata, create_class_name_to_index, create_one_type_dictionary, \
    update_class_distribution, update_feature_distributions, validate_class_distribution, validate_num_samples

NUM_SAMPLES = 12960

VARIABLES = [
    "parents",
    "has_nurs",
    "form",
    "children",
    "housing",
    "finance",
    "social",
    "health",
]

VALUES = {
    "parents": ["usual", "pretentious", "great_pret"],
    "has_nurs": ["proper", "less_proper", "improper", "critical", "very_crit"],
    "form": ["complete", "completed", "incomplete", "foster"],
    "children": ["1", "2", "3", "more"],
    "housing": ["convenient", "less_conv", "critical"],
    "finance": ["convenient", "inconv"],
    "social": ["nonprob", "slightly_prob", "problematic"],
    "health": ["recommended", "priority", "not_recom"],
}

CLASSES = [
    "not_recom",
    "recommend",
    "very_recom",
    "priority",
    "spec_prior"
]

CLASS_TO_INDEX = create_class_name_to_index(CLASSES)


def nursery_transform(input_path, features_path, labels_path, metadata_path):
    input_file = open(input_path, "r")
    reader = csv.DictReader(input_file, fieldnames=VARIABLES + ["class"])

    metadata = create_metadata(VARIABLES,
                               create_one_type_dictionary("categorical", VARIABLES),
                               VALUES,
                               NUM_SAMPLES,
                               CLASSES)

    # initialize outputs
    features = np.zeros((metadata["num_samples"], metadata["num_features"]), dtype=np.uint8)
    labels = np.zeros(metadata["num_samples"], dtype=np.int32)

    # transform
    sample_index = 0
    for row in reader:
        labels[sample_index] = CLASS_TO_INDEX[row["class"]]

        for variable in VARIABLES:
            value = row[variable]
            assert value in VALUES[variable], "'{}' is not a valid value for '{}'".format(value, variable)
            feature_index = metadata["value_to_index"][variable][value]
            features[sample_index, feature_index] = 1

        # next row
        sample_index += 1

    # add distributions to the metadata
    update_feature_distributions(metadata, features)
    update_class_distribution(metadata, labels)

    # validate the known distributions
    validate_num_samples(metadata, sample_index)

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

    options = options_parser.parse_args(args=args)

    nursery_transform(options.input, options.features, options.labels, options.metadata)


if __name__ == "__main__":
    main()
