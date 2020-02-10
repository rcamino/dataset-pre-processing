from __future__ import print_function

import argparse
import json

import numpy as np

from dataset_pre_processing.metadata import create_metadata, create_class_to_index

from sklearn.preprocessing import MinMaxScaler


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
    "workclass":{
        "Private",
        "Self-emp-not-inc",
        "Self-emp-inc",
        "Federal-gov",
        "Local-gov",
        "State-gov",
        "Without-pay",
        "Never-worked"
    },
    "education":{
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
    "marital-status":{
        "Married-civ-spouse",
        "Divorced",
        "Never-married",
        "Separated",
        "Widowed",
        "Married-spouse-absent",
        "Married-AF-spouse"
    },
    "occupation":{
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
    "relationship":{
        "Wife",
        "Own-child",
        "Husband",
        "Not-in-family",
        "Other-relative",
        "Unmarried"
    },
    "race":{
        "White",
        "Asian-Pac-Islander",
        "Amer-Indian-Eskimo",
        "Other",
        "Black"
    },
    "sex":{
        "Female",
        "Male"
    },
    "native-country":{
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

CLASS_TO_INDEX = create_class_to_index(CLASSES)

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


def adult_transform(input_train_path, input_test_path, features_train_path, features_test_path, labels_train_path,
                    labels_test_path, metadata_path, ignore_missing):

    num_samples_train = NUM_SAMPLES[ignore_missing]["train"]
    num_samples_test = NUM_SAMPLES[ignore_missing]["test"]

    metadata = create_metadata(VARIABLES, TYPES, VALUES, num_samples_train + num_samples_test, CLASSES)

    # transform train
    train_file = open(input_train_path, "r")
    features_train, labels_train = adult_transform_file(train_file,
                                                        num_samples_train,
                                                        metadata["num_features"],
                                                        metadata["value_to_index"],
                                                        ignore_missing)
    train_file.close()

    # transform test
    test_file = open(input_test_path, "r")
    test_file.readline()  # has an extra first line
    features_test, labels_test = adult_transform_file(test_file,
                                                      num_samples_test,
                                                      metadata["num_features"],
                                                      metadata["value_to_index"],
                                                      ignore_missing)
    test_file.close()

    # scale train and test together
    features = np.concatenate((features_train, features_test))
    scaler = MinMaxScaler(feature_range=(0, 1), copy=False)
    scaler.fit(features)
    scaler.transform(features_train)
    scaler.transform(features_test)

    # save
    np.save(features_train_path, features_train)
    np.save(labels_train_path, labels_train)
    np.save(features_test_path, features_test)
    np.save(labels_test_path, labels_test)

    metadata["features_min"] = scaler.data_min_.tolist()
    metadata["features_max"] = scaler.data_max_.tolist()

    with open(metadata_path, "w") as metadata_file:
        json.dump(metadata, metadata_file)


def adult_transform_file(input_file, num_samples, num_features, value_to_index, ignore_missing):
    features = np.zeros((num_samples, num_features), dtype=np.float32)
    labels = np.zeros(num_samples, dtype=np.int32)
    i = 0
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
                    features[i, value_to_index[variable]] = value
                elif TYPES[variable] == "categorical":
                    if value == "?" or value == "":
                        for possible_value in value_to_index[variable].keys():
                            features[i, value_to_index[variable][possible_value]] = np.nan
                    else:  # set all the value as nan
                        assert value in VALUES[variable],\
                            "'{}' is not a valid value for '{}'".format(value, variable)
                        features[i, value_to_index[variable][value]] = 1.0

            # the last value is the class
            labels[i] = CLASS_TO_INDEX[values[-1]]

            i += 1

        line = input_file.readline()

    assert i == num_samples

    return features, labels


def main(args=None):
    options_parser = argparse.ArgumentParser(
        description="Transform the Adult text train and test data into feature matrices."
                    + " Dataset: http://mlr.cs.umass.edu/ml/datasets/Adult."
    )

    options_parser.add_argument("input_train", type=str, help="Input Adult train data in text format.")
    options_parser.add_argument("input_test", type=str, help="Input Adult test data in text format.")
    options_parser.add_argument("features_train", type=str, help="Output train features in numpy array format.")
    options_parser.add_argument("features_test", type=str, help="Output test features in numpy array format.")
    options_parser.add_argument("labels_train", type=str, help="Output train labels in numpy array format.")
    options_parser.add_argument("labels_test", type=str, help="Output test labels in numpy array format.")
    options_parser.add_argument("metadata", type=str, help="Metadata in json format.")

    options_parser.add_argument("--ignore_missing", action="store_true", help="Ignore rows with missing values.")

    options = options_parser.parse_args(args=args)

    adult_transform(options.input_train,
                    options.input_test,
                    options.features_train,
                    options.features_test,
                    options.labels_train,
                    options.labels_test,
                    options.metadata,
                    options.ignore_missing)


if __name__ == "__main__":
    main()
