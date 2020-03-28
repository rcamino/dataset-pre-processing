from collections import Counter

import numpy as np


CATEGORICAL_FEATURE_FORMAT = "{}_{:d}"


def create_one_type_dictionary(variable_type, variables):
    return dict([(variable, variable_type) for variable in variables])


def types_to_sorted_lists(variable_types, variables=None):
    if variables is None:
        variables = variable_types.keys()

    binary_variables = []
    categorical_variables = []
    numerical_variables = []
    for variable in variables:
        variable_type = variable_types[variable]
        if variable_type == "binary":
            binary_variables.append(variable)
        elif variable_type == "categorical":
            categorical_variables.append(variable)
        elif variable_type == "numerical":
            numerical_variables.append(variable)
        else:
            raise Exception("Invalid type: '{}'.".format(variable_type))

    binary_variables = sorted(binary_variables)
    categorical_variables = sorted(categorical_variables)
    numerical_variables = sorted(numerical_variables)
    return binary_variables, categorical_variables, numerical_variables


def create_metadata(variables, variable_types, categorical_values={}, num_samples=None, classes=None):
    binary_variables, categorical_variables, numerical_variables = types_to_sorted_lists(variable_types, variables)

    sorted_variables = []
    feature_number = 0
    features = []
    value_to_index = {}
    index_to_value = []
    variable_sizes = []
    variable_types = []

    for variable in binary_variables:
        sorted_variables.append(variable)
        variable_types.append("binary")
        variable_sizes.append(1)
        value_to_index[variable] = feature_number
        feature_number += 1
        features.append(variable)

    for variable in categorical_variables:
        sorted_variables.append(variable)
        variable_types.append("categorical")
        values = sorted(categorical_values[variable])
        variable_sizes.append(len(values))
        value_to_index[variable] = {}
        for value_index, value in enumerate(values):
            index_to_value.append((variable, value))
            value_to_index[variable][value] = feature_number
            feature_number += 1
            features.append(CATEGORICAL_FEATURE_FORMAT.format(variable, value_index))

    for variable in numerical_variables:
        sorted_variables.append(variable)
        variable_types.append("numerical")
        variable_sizes.append(1)
        value_to_index[variable] = feature_number
        feature_number += 1
        features.append(variable)

    num_features = feature_number

    metadata = {
        "variables": sorted_variables,
        "features": features,
        "variable_sizes": variable_sizes,
        "variable_types": variable_types,
        "index_to_value": index_to_value,
        "value_to_index": value_to_index,
        "num_features": num_features,
        "num_variables": len(sorted_variables),
        "num_binary_variables": len(binary_variables),
        "num_categorical_variables": len(categorical_variables),
        "num_numerical_variables": len(numerical_variables),
    }

    if num_samples is not None:
        metadata["num_samples"] = num_samples

    if classes is not None:
        metadata["classes"] = classes
        metadata["num_classes"] = len(classes)

    return metadata


def create_class_name_to_index(classes):
    return dict([(c, i) for i, c in enumerate(classes)])


def update_feature_distributions(metadata, features):
    # I use float and int instead of numpy types because they are not JSON serializable
    metadata["variable_distributions"] = {}
    for variable, variable_type in zip(metadata["variables"], metadata["variable_types"]):
        metadata["variable_distributions"][variable] = create_feature_distribution(features,
                                                                                   variable_type,
                                                                                   metadata["value_to_index"][variable])


def create_feature_distribution(features, variable_type, variable_value_to_index):
    if variable_type == "binary":
        ones = int(np.sum(features[:, variable_value_to_index]))
        return {0: len(features) - ones, 1: ones}
    elif variable_type == "categorical":
        distribution = {}
        for value, feature_number in variable_value_to_index.items():
            distribution[value] = int(np.sum(features[:, feature_number]))
    elif variable_type == "numerical":
        return {
            "median": float(np.median(features[:, variable_value_to_index])),
            "mean": float(np.mean(features[:, variable_value_to_index])),
            "std": float(np.std(features[:, variable_value_to_index])),
            "min": float(np.min(features[:, variable_value_to_index])),
            "max": float(np.max(features[:, variable_value_to_index])),
        }
    else:
        raise Exception("Invalid variable type '{}'.".format(variable_type))


def update_class_distribution(metadata, labels):
    assert "classes" in metadata
    samples_by_class_index = Counter(labels)
    metadata["class_distribution"] = {}
    for class_index, class_name in enumerate(metadata["classes"]):
        metadata["class_distribution"][class_name] = samples_by_class_index[class_index]


def validate_class_distribution(metadata, samples_by_class_index):
    assert "class_distribution" in metadata
    class_name_to_index = create_class_name_to_index(metadata["class_distribution"])
    for class_name, class_index in class_name_to_index.items():
        assert metadata["class_distribution"][class_name] == samples_by_class_index[class_index]


def validate_num_samples(metadata, num_samples):
    assert metadata["num_samples"] == num_samples
