import argparse
import json
import os

import numpy as np


def main(args=None):
    options_parser = argparse.ArgumentParser(description="Split features by class.")

    options_parser.add_argument("features", type=str, help="Input features in numpy array format.")
    options_parser.add_argument("labels", type=str, help="Input labels in numpy array format.")
    options_parser.add_argument("input_metadata", type=str, help="Input metadata in json format.")
    options_parser.add_argument("output_directory", type=str, help="Directory path to save feature outputs.")

    options_parser.add_argument("output_template", type=str,
                                help="Output file name template. Variables: number, total.")

    options_parser.add_argument("output_metadata", type=str,
                                help="Output metadata in json format. It has no class information or number of samples,"
                                     + " so it can be used by any output subset.")

    options = options_parser.parse_args(args=args)

    features = np.load(options.features)
    labels = np.load(options.labels)

    with open(options.input_metadata, "r") as metadata_file:
        metadata = json.load(metadata_file)

    assert "classes" in metadata, "Metadata needs class information."

    template = os.path.join(options.output_directory, options.output_template)
    num_classes = len(metadata["classes"])

    # create and save one subset by class
    for class_index, class_value in enumerate(metadata["classes"]):
        class_samples_index = labels == class_index
        class_num_samples = sum(class_samples_index)

        if class_num_samples == 0:
            print("WARNING: Class number {:d} ({}) has no samples.".format(class_index, class_value))
        else:
            class_features = features[class_samples_index, :]
            np.save(template.format(number=class_index, total=num_classes), class_features)

    # remove number of samples from metadata
    if "num_samples" in metadata:
        metadata.pop("num_samples")

    # remove class information from metadata
    metadata.pop("classes")
    metadata.pop("num_classes")

    # save the modified metadata
    with open(options.output_metadata, "w") as metadata_file:
        json.dump(metadata, metadata_file)


if __name__ == "__main__":
    main()
