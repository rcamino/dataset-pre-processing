from __future__ import print_function

import argparse
import json
import pickle

import numpy as np

from dataset_pre_processing.metadata import create_metadata

from sklearn.preprocessing import MinMaxScaler


VARIABLES = [
    "Elevation",
    "Aspect",
    "Slope",
    "Horizontal_Distance_To_Hydrology",
    "Vertical_Distance_To_Hydrology",
    "Horizontal_Distance_To_Roadways",
    "Hillshade_9am",
    "Hillshade_Noon",
    "Hillshade_3pm",
    "Horizontal_Distance_To_Fire_Points",
    "Wilderness_Area",
    "Soil_Type",
]

TYPES = {
    "Elevation": "numerical",
    "Aspect": "numerical",
    "Slope": "numerical",
    "Horizontal_Distance_To_Hydrology": "numerical",
    "Vertical_Distance_To_Hydrology": "numerical",
    "Horizontal_Distance_To_Roadways": "numerical",
    "Hillshade_9am": "numerical",
    "Hillshade_Noon": "numerical",
    "Hillshade_3pm": "numerical",
    "Horizontal_Distance_To_Fire_Points": "numerical",
    "Wilderness_Area": "categorical",
    "Soil_Type": "categorical",
}

VALUES = {
    "Wilderness_Area": [
        "Rawah Wilderness Area",
        "Neota Wilderness Area",
        "Comanche Peak Wilderness Area",
        "Cache la Poudre Wilderness Area"
    ],
    "Soil_Type": [
        "Cathedral family - Rock outcrop complex, extremely stony",
        "Vanet - Ratake families complex, very stony",
        "Haploborolis - Rock outcrop complex, rubbly",
        "Ratake family - Rock outcrop complex, rubbly",
        "Vanet family - Rock outcrop complex complex, rubbly",
        "Vanet - Wetmore families - Rock outcrop complex, stony",
        "Gothic family",
        "Supervisor - Limber families complex",
        "Troutville family, very stony",
        "Bullwark - Catamount families - Rock outcrop complex, rubbly",
        "Bullwark - Catamount families - Rock land complex, rubbly",
        "Legault family - Rock land complex, stony",
        "Catamount family - Rock land - Bullwark family complex, rubbly",
        "Pachic Argiborolis - Aquolis complex",
        "unspecified in the USFS Soil and ELU Survey",
        "Cryaquolis - Cryoborolis complex",
        "Gateview family - Cryaquolis complex",
        "Rogert family, very stony",
        "Typic Cryaquolis - Borohemists complex",
        "Typic Cryaquepts - Typic Cryaquolls complex",
        "Typic Cryaquolls - Leighcan family, till substratum complex",
        "Leighcan family, till substratum, extremely bouldery",
        "Leighcan family, till substratum - Typic Cryaquolls complex",
        "Leighcan family, extremely stony",
        "Leighcan family, warm, extremely stony",
        "Granile - Catamount families complex, very stony",
        "Leighcan family, warm - Rock outcrop complex, extremely stony",
        "Leighcan family - Rock outcrop complex, extremely stony",
        "Como - Legault families complex, extremely stony",
        "Como family - Rock land - Legault family complex, extremely stony",
        "Leighcan - Catamount families complex, extremely stony",
        "Catamount family - Rock outcrop - Leighcan family complex, extremely stony",
        "Leighcan - Catamount families - Rock outcrop complex, extremely stony",
        "Cryorthents - Rock land complex, extremely stony",
        "Cryumbrepts - Rock outcrop - Cryaquepts complex",
        "Bross family - Rock land - Cryumbrepts complex, extremely stony",
        "Rock outcrop - Cryumbrepts - Cryorthents complex, extremely stony",
        "Leighcan - Moran families - Cryaquolls complex, extremely stony",
        "Moran family - Cryorthents - Leighcan family complex, extremely stony",
        "Moran family - Cryorthents - Rock land complex, extremely stony",
    ]
}

NUM_SAMPLES = [
    211840,
    283301,
    35754,
    2747,
    9493,
    17367,
    20510
]

CLASSES = [
    "Spruce/Fir",
    "Lodgepole Pine",
    "Ponderosa Pine",
    "Cottonwood/Willow",
    "Aspen",
    "Douglas-fir",
    "Krummholz"
]


def covertype_transform(input_path, features_path, labels_path, metadata_path, scaler_path):
    metadata = create_metadata(VARIABLES, TYPES, VALUES, sum(NUM_SAMPLES), CLASSES)

    # The raw data is already nicely one-hot-encoded, but we need to follow the standard of our metadata.
    # The most important thing is that we put the categorical features at the beginning.
    # The extra annoying thing is that we also sort the categorical values alphabetically.
    # Because of this, we need to do map of feature indices unnecessarily.
    old_to_new_feature_indices = {}
    old_feature_index = 0
    for variable in VARIABLES:
        if TYPES[variable] == "numerical":
            old_to_new_feature_indices[old_feature_index] = metadata["value_to_index"][variable]
            old_feature_index += 1
        elif TYPES[variable] == "categorical":
            for value in VALUES[variable]:
                old_to_new_feature_indices[old_feature_index] = metadata["value_to_index"][variable][value]
                old_feature_index += 1
        else:
            raise Exception("Invalid type.")

    input_file = open(input_path, "r")

    features = np.zeros((metadata["num_samples"], metadata["num_features"]), dtype=np.float32)
    labels = np.zeros(metadata["num_samples"], dtype=np.int32)

    # transform
    sample_index = 0
    line = input_file.readline()
    while line != "":
        line = line.rstrip("\n")
        values = line.split(",")

        # transform original class numbers to 0 indexed arrays
        class_number = int(values[-1]) - 1

        if sample_index < metadata["num_samples"]:
            # the categorical variables are already one hot encoded
            for old_feature_index, value in enumerate(values[:-1]):
                new_feature_index = old_to_new_feature_indices[old_feature_index]
                value = float(value)
                features[sample_index, new_feature_index] = value

            # the class needs to be transformed
            labels[sample_index] = class_number

        sample_index += 1

        line = input_file.readline()

    # scale
    if scaler_path is not None:
        scaler = MinMaxScaler(feature_range=(0, 1), copy=False)
        scaler.fit_transform(features)

        with open(scaler_path, "wb") as scaler_file:
            pickle.dump(scaler, scaler_file)

    assert sample_index == metadata["num_samples"]

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

    covertype_transform(options.input,
                        options.features,
                        options.labels,
                        options.metadata,
                        options.scaler)


if __name__ == "__main__":
    main()
