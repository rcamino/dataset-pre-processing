import argparse
import json

import numpy as np

from dataset_pre_processing.metadata import create_metadata, create_class_name_to_index, update_feature_distributions, \
    update_class_distribution
from dataset_pre_processing.scaling import scale_and_save_scaler


VARIABLES = [
    "age",
    "workclass",
    "fnlwgt",
    "education",
    "education-num",
    "marital-status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "capital-gain",
    "capital-loss",
    "hours-per-week",
    "native-country",
]

TYPES = {
    "age": "numerical",
    "workclass": "categorical",
    "fnlwgt": "numerical",
    "education": "categorical",
    "education-num": "numerical",
    "marital-status": "categorical",
    "occupation": "categorical",
    "relationship": "categorical",
    "race": "categorical",
    "sex": "categorical",
    "capital-gain": "numerical",
    "capital-loss": "numerical",
    "hours-per-week": "numerical",
    "native-country": "categorical",
}

VALUES = {
    "workclass": {
        "Private",
        "Self-emp-not-inc",
        "Self-emp-inc",
        "Federal-gov",
        "Local-gov",
        "State-gov",
        "Without-pay",
        "Never-worked"
    },
    "education": {
        "Bachelors",
        "Some-college",
        "11th",
        "HS-grad",
        "Prof-school",
        "Assoc-acdm",
        "Assoc-voc",
        "9th",
        "7th-8th",
        "12th",
        "Masters",
        "1st-4th",
        "10th",
        "Doctorate",
        "5th-6th",
        "Preschool"
    },
    "marital-status": {
        "Married-civ-spouse",
        "Divorced",
        "Never-married",
        "Separated",
        "Widowed",
        "Married-spouse-absent",
        "Married-AF-spouse"
    },
    "occupation": {
        "Tech-support",
        "Craft-repair",
        "Other-service",
        "Sales",
        "Exec-managerial",
        "Prof-specialty",
        "Handlers-cleaners",
        "Machine-op-inspct",
        "Adm-clerical",
        "Farming-fishing",
        "Transport-moving",
        "Priv-house-serv",
        "Protective-serv",
        "Armed-Forces"
    },
    "relationship": {
        "Wife",
        "Own-child",
        "Husband",
        "Not-in-family",
        "Other-relative",
        "Unmarried"
    },
    "race": {
        "White",
        "Asian-Pac-Islander",
        "Amer-Indian-Eskimo",
        "Other",
        "Black"
    },
    "sex": {
        "Female",
        "Male"
    },
    "native-country": {
        "United-States",
        "Cambodia",
        "England",
        "Puerto-Rico",
        "Canada",
        "Germany",
        "Outlying-US(Guam-USVI-etc)",
        "India",
        "Japan",
        "Greece",
        "South",
        "China",
        "Cuba",
        "Iran",
        "Honduras",
        "Philippines",
        "Italy",
        "Poland",
        "Jamaica",
        "Vietnam",
        "Mexico",
        "Portugal",
        "Ireland",
        "France",
        "Dominican-Republic",
        "Laos",
        "Ecuador",
        "Taiwan",
        "Haiti",
        "Columbia",
        "Hungary",
        "Guatemala",
        "Nicaragua",
        "Scotland",
        "Thailand",
        "Yugoslavia",
        "El-Salvador",
        "Trinadad&Tobago",
        "Peru",
        "Hong",
        "Holand-Netherlands"
    }
}

CLASSES = [
    "<=50K",
    ">50K"
]

CLASS_TO_INDEX = create_class_name_to_index(CLASSES)

NUM_SAMPLES = {
    False: {  # all rows
        "train": 32561,
        "test": 16281,
    },
    True: {  # ignoring rows with missing values
        "train": 30162,
        "test": 15060,
    }
}


def transform(train_path, test_path, features_path, labels_path, metadata_path, ignore_missing, scaler_path):

    num_samples_train = NUM_SAMPLES[ignore_missing]["train"]
    num_samples_test = NUM_SAMPLES[ignore_missing]["test"]

    metadata = create_metadata(VARIABLES, TYPES, VALUES, num_samples_train + num_samples_test, CLASSES)

    # transform train
    train_file = open(train_path, "r")
    features_train, labels_train = adult_transform_file(train_file,
                                                        num_samples_train,
                                                        metadata["num_features"],
                                                        metadata["value_to_index"],
                                                        ignore_missing)
    train_file.close()

    # transform test
    test_file = open(test_path, "r")
    test_file.readline()  # has an extra first line
    features_test, labels_test = adult_transform_file(test_file,
                                                      num_samples_test,
                                                      metadata["num_features"],
                                                      metadata["value_to_index"],
                                                      ignore_missing)
    test_file.close()

    # concatenate train and test
    features = np.concatenate((features_train, features_test))
    labels = np.concatenate((labels_train, labels_test))

    # scale
    if scaler_path is not None:
        features = scale_and_save_scaler(features, scaler_path)

    # add distributions to the metadata
    update_feature_distributions(metadata, features)
    update_class_distribution(metadata, labels)

    # save
    np.save(features_path, features)
    np.save(labels_path, labels)

    with open(metadata_path, "w") as metadata_file:
        json.dump(metadata, metadata_file)


def adult_transform_file(input_file, num_samples, num_features, value_to_index, ignore_missing):
    # initialize outputs
    features = np.zeros((num_samples, num_features), dtype=np.float32)
    labels = np.zeros(num_samples, dtype=np.int32)

    # transform
    sample_index = 0
    line = input_file.readline()
    while line != "":
        line = line.rstrip("\n.")
        values = line.split(", ")

        missing_values = False
        for value in values:
            if value == "?" or value == "":
                missing_values = True
                break

        # if there are missing values the ignore missing flag is set then ignore the row
        if not missing_values or not ignore_missing:
            # iterate variable values (except the last one)
            for variable, value in zip(VARIABLES, values[:-1]):
                if TYPES[variable] == "numerical":
                    if value == "?" or value == "":
                        value = np.nan
                    else:
                        value = float(value)
                    features[sample_index, value_to_index[variable]] = value
                elif TYPES[variable] == "categorical":
                    if value == "?" or value == "":
                        for possible_value in value_to_index[variable].keys():
                            features[sample_index, value_to_index[variable][possible_value]] = np.nan
                    else:  # set all the value as nan
                        assert value in VALUES[variable],\
                            "'{}' is not a valid value for '{}'".format(value, variable)
                        features[sample_index, value_to_index[variable][value]] = 1.0

            # the last value is the class
            labels[sample_index] = CLASS_TO_INDEX[values[-1]]

            # next row (only here when the value was used)
            sample_index += 1

        # next line
        line = input_file.readline()

    # validate number of samples
    assert sample_index == num_samples

    return features, labels


def main(args=None):
    options_parser = argparse.ArgumentParser(
        description="Transform the text train and test data into a feature matrix and label array.")

    options_parser.add_argument("train", type=str, help="Input train data in text format.")
    options_parser.add_argument("test", type=str, help="Input test data in text format.")
    options_parser.add_argument("features", type=str, help="Output features in numpy array format.")
    options_parser.add_argument("labels", type=str, help="Output labels in numpy array format.")
    options_parser.add_argument("metadata", type=str, help="Metadata in json format.")

    options_parser.add_argument("--ignore_missing", action="store_true", help="Ignore rows with missing values.")

    options_parser.add_argument("--scaler", type=str,
                                help="Output scikit-learn MinMaxScaler in pickle format. Enables scaling to (0, 1).")

    options = options_parser.parse_args(args=args)

    transform(options.train,
              options.test,
              options.features,
              options.labels,
              options.metadata,
              options.ignore_missing,
              options.scaler)


if __name__ == "__main__":
    main()
