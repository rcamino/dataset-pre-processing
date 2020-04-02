import argparse
import json


def print_metadata(metadata):
    print("Sizes:")
    print("---")

    keys = [
        "num_classes",
        "num_samples",
        "num_features",
        "num_variables",
        "num_binary_variables",
        "num_categorical_variables",
        "num_numerical_variables",
    ]

    for key in keys:
        if key in metadata:
            print(key, metadata[key])

    print()

    print("Variables:")
    print("---")
    print("Index | Name | Type | Size | Feature Range")
    print("---")

    feature_index = 0

    for variable_index, (variable, variable_type, variable_size) in \
            enumerate(zip(metadata["variables"], metadata["variable_types"], metadata["variable_sizes"])):

        feature_limit = feature_index + variable_size

        print("{:d} | {} | {} | {:d} | [{:d}; {:d}]".format(variable_index,
                                                            variable,
                                                            variable_type,
                                                            variable_size,
                                                            feature_index, feature_limit - 1,))
        feature_index = feature_limit


def main(args=None):
    options_parser = argparse.ArgumentParser(description="Print metadata.")

    options_parser.add_argument("metadata", type=str, help="Metadata in json format.")

    options = options_parser.parse_args(args=args)

    with open(options.metadata, "r") as metadata_file:
        metadata = json.load(metadata_file)

    print_metadata(metadata)


if __name__ == "__main__":
    main()
