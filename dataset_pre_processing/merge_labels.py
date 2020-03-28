import argparse
import json

from copy import deepcopy

import numpy as np

from dataset_pre_processing.metadata import CATEGORICAL_FEATURE_FORMAT


def merge_labels(features, labels, metadata, variable):
    # validate input shapes
    num_samples, num_features = features.shape
    assert len(labels) == num_samples
    assert sum(metadata["variable_sizes"]) == metadata["num_features"] == num_features

    # validate labels
    num_classes = len(set(labels))
    assert "classes" in metadata and "num_classes" in metadata and "class_distribution" in metadata
    assert len(metadata["classes"]) == metadata["num_classes"] == num_classes

    # if it is multi-class
    if num_classes > 2:
        variable_type = "categorical"
        variable_size = num_classes
    # if it is binary class
    elif num_classes == 2:
        variable_type = "binary"
        variable_size = 1
    # something went wrong
    else:
        raise Exception("Invalid number of classes {:d}.".format(num_classes))

    # create the output metadata based on the input metadata
    output_metadata = deepcopy(metadata)

    # add class variable to the metadata
    output_metadata["variables"].append(variable)
    output_metadata["variable_types"].append(variable_type)
    output_metadata["variable_sizes"].append(variable_size)
    output_metadata["num_variables"] += 1

    # next available feature index
    feature_index = num_features

    # if it is categorical
    if variable_type == "categorical":
        # concatenate the one-hot-encoding
        variable_features = np.zeros((num_samples, variable_size), dtype=np.float32)
        variable_features[labels] = 1
        output_features = np.concatenate((features, variable_features), axis=1)

        # add categorical variable metadata
        output_metadata["num_categorical_variables"] += 1

        output_metadata["value_to_index"][variable] = {}
        for class_index, class_value in enumerate(metadata["classes"]):
            output_metadata["index_to_value"].append((variable, class_value))
            output_metadata["value_to_index"][variable][class_value] = feature_index
            output_metadata["num_features"] += 1
            output_metadata["features"].append(CATEGORICAL_FEATURE_FORMAT.format(variable, class_index))
            feature_index += 1
    # if it is binary
    else:
        # concatenate the labels
        output_features = np.concatenate((features, labels.reshape(-1, 1)), axis=1)

        # add binary variable metadata
        output_metadata["value_to_index"][variable] = feature_index
        output_metadata["num_features"] += 1
        output_metadata["features"].append(variable)
        output_metadata["num_binary_variables"] += 1

    # transform the class distribution into the variable distribution
    output_metadata["variable_distributions"][variable] = output_metadata["class_distribution"]

    # remove class information
    output_metadata.pop("classes")
    output_metadata.pop("num_classes")
    output_metadata.pop("class_distribution")

    # validate output shape
    assert sum(output_metadata["variable_sizes"]) == output_metadata["num_features"] == output_features.shape[1]

    return output_features, output_metadata


def main():
    options_parser = argparse.ArgumentParser(description="Merge labels into the features as a new variable.")

    options_parser.add_argument("input_features", type=str, help="Input features in numpy array format.")
    options_parser.add_argument("input_labels", type=str, help="Input labels in numpy array format.")
    options_parser.add_argument("input_metadata", type=str, help="Input metadata in json format.")
    options_parser.add_argument("output_features", type=str, help="Output features file.")
    options_parser.add_argument("output_metadata", type=str, help="Output metadata in json format.")

    options_parser.add_argument("--variable", type=str, help="Name of the merged variable.", default="class")

    options = options_parser.parse_args()

    features = np.load(options.input_features)
    labels = np.load(options.input_labels)

    with open(options.input_metadata, "r") as metadata_file:
        metadata = json.load(metadata_file)

    output_features, output_metadata = merge_labels(features, labels, metadata, options.variable)

    np.save(options.output_features, output_features)

    with open(options.output_metadata, "w") as metadata_file:
        json.dump(output_metadata, metadata_file)


if __name__ == "__main__":
    main()
