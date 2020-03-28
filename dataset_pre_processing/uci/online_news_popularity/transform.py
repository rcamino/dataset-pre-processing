import argparse
import csv
import json

import numpy as np

from dataset_pre_processing.metadata import create_metadata, update_feature_distributions, validate_num_samples
from dataset_pre_processing.scaling import scale_and_save_scaler


NUM_SAMPLES = 39644

ORIGINAL_TYPES = {
    "n_tokens_title": "numerical",  # Number of words in the title
    "n_tokens_content": "numerical",  # Number of words in the content
    "n_unique_tokens": "numerical",  # Rate of unique words in the content
    "n_non_stop_words": "numerical",  # Rate of non-stop words in the content
    "n_non_stop_unique_tokens": "numerical",  # Rate of unique non-stop words in the content
    "num_hrefs": "numerical",  # Number of links
    "num_self_hrefs": "numerical",  # Number of links to other articles published by Mashable
    "num_imgs": "numerical",  # Number of images
    "num_videos": "numerical",  # Number of videos
    "average_token_length": "numerical",  # Average length of the words in the content
    "num_keywords": "numerical",  # Number of keywords in the metadata
    "data_channel_is_lifestyle": "binary",  # Is data channel 'Lifestyle'?
    "data_channel_is_entertainment": "binary",  # Is data channel 'Entertainment'?
    "data_channel_is_bus": "binary",  # Is data channel 'Business'?
    "data_channel_is_socmed": "binary",  # Is data channel 'Social Media'?
    "data_channel_is_tech": "binary",  # Is data channel 'Tech'?
    "data_channel_is_world": "binary",  # Is data channel 'World'?
    "kw_min_min": "numerical",  # Worst keyword (min. shares)
    "kw_max_min": "numerical",  # Worst keyword (max. shares)
    "kw_avg_min": "numerical",  # Worst keyword (avg. shares)
    "kw_min_max": "numerical",  # Best keyword (min. shares)
    "kw_max_max": "numerical",  # Best keyword (max. shares)
    "kw_avg_max": "numerical",  # Best keyword (avg. shares)
    "kw_min_avg": "numerical",  # Avg. keyword (min. shares)
    "kw_max_avg": "numerical",  # Avg. keyword (max. shares)
    "kw_avg_avg": "numerical",  # Avg. keyword (avg. shares)
    "self_reference_min_shares": "numerical",  # Min. shares of referenced articles in Mashable
    "self_reference_max_shares": "numerical",  # Max. shares of referenced articles in Mashable
    "self_reference_avg_sharess": "numerical",  # Avg. shares of referenced articles in Mashable
    "weekday_is_monday": "binary",  # Was the article published on a Monday?
    "weekday_is_tuesday": "binary",  # Was the article published on a Tuesday?
    "weekday_is_wednesday": "binary",  # Was the article published on a Wednesday?
    "weekday_is_thursday": "binary",  # Was the article published on a Thursday?
    "weekday_is_friday": "binary",  # Was the article published on a Friday?
    "weekday_is_saturday": "binary",  # Was the article published on a Saturday?
    "weekday_is_sunday": "binary",  # Was the article published on a Sunday?
    "is_weekend": "binary",  # Was the article published on the weekend?
    "LDA_00": "numerical",  # Closeness to LDA topic 0
    "LDA_01": "numerical",  # Closeness to LDA topic 1
    "LDA_02": "numerical",  # Closeness to LDA topic 2
    "LDA_03": "numerical",  # Closeness to LDA topic 3
    "LDA_04": "numerical",  # Closeness to LDA topic 4
    "global_subjectivity": "numerical",  # Text subjectivity
    "global_sentiment_polarity": "numerical",  # Text sentiment polarity
    "global_rate_positive_words": "numerical",  # Rate of positive words in the content
    "global_rate_negative_words": "numerical",  # Rate of negative words in the content
    "rate_positive_words": "numerical",  # Rate of positive words among non-neutral tokens
    "rate_negative_words": "numerical",  # Rate of negative words among non-neutral tokens
    "avg_positive_polarity": "numerical",  # Avg. polarity of positive words
    "min_positive_polarity": "numerical",  # Min. polarity of positive words
    "max_positive_polarity": "numerical",  # Max. polarity of positive words
    "avg_negative_polarity": "numerical",  # Avg. polarity of negative  words
    "min_negative_polarity": "numerical",  # Min. polarity of negative  words
    "max_negative_polarity": "numerical",  # Max. polarity of negative  words
    "title_subjectivity": "numerical",  # Title subjectivity
    "title_sentiment_polarity": "numerical",  # Title polarity
    "abs_title_subjectivity": "numerical",  # Absolute subjectivity level
    "abs_title_sentiment_polarity": "numerical",  # Absolute polarity level
}

CAN_BE_EMPTY = {
    "data_channel": True,
    "weekday": False,
}

ONE_HOT_ENCODING_SEPARATOR = "_is_"


def read_binary(value):
    return int(float(value.strip()))


def build_mappings():
    variables = []
    types = {}
    values = {}
    for original_variable, original_type in ORIGINAL_TYPES.items():
        # if it is one of the one-hot-encoded categorical variables
        if original_type == "binary" and ONE_HOT_ENCODING_SEPARATOR in original_variable:
            # split into variable and value
            separator_index = original_variable.index(ONE_HOT_ENCODING_SEPARATOR)
            variable = original_variable[:separator_index]
            value = original_variable[separator_index + len(ONE_HOT_ENCODING_SEPARATOR):]

            # if it is the first time for this categorical variable
            if variable not in types:
                assert variable not in values
                types[variable] = "categorical"

                # initialize the categorical variable values
                if CAN_BE_EMPTY[variable]:
                    values[variable] = ["none"]
                else:
                    values[variable] = []

                # add the categorical variable
                variables.append(variable)

            # add the new value for the categorical variable
            values[variable].append(value)
        # if it is one of the non-one-hot-encoded categorical variables (numerical or the only one that is binary)
        else:
            # identity mapping
            variables.append(original_variable)
            types[original_variable] = original_type

    return variables, types, values


VARIABLES, TYPES, VALUES = build_mappings()


def online_news_popularity_transform(input_path, features_path, labels_path, metadata_path, scaler_path):
    metadata = create_metadata(VARIABLES, TYPES, VALUES, NUM_SAMPLES)

    input_file = open(input_path, "r")
    reader = csv.DictReader(input_file)

    reader.fieldnames = [variable.strip() for variable in reader.fieldnames]

    # initialize outputs
    features = np.zeros((metadata["num_samples"], metadata["num_features"]), dtype=np.float32)
    labels = np.zeros(metadata["num_samples"], dtype=np.float32)

    # transform
    sample_index = 0
    for row in reader:
        for variable in metadata["variables"]:
            # numerical variable
            if TYPES[variable] == "numerical":
                value = float(row[variable])
                features[sample_index, metadata["value_to_index"][variable]] = value

            # categorical variable
            elif TYPES[variable] == "categorical":
                value = None

                # check all possible values
                for possible_value in VALUES[variable]:
                    # skip the none possible value
                    if possible_value == "none":
                        continue

                    # if the possible value binary flag is set
                    real_variable = "{}{}{}".format(variable, ONE_HOT_ENCODING_SEPARATOR, possible_value)
                    if read_binary(row[real_variable]) == 1:
                        # if the categorical variable had no value set
                        if value is None:
                            value = possible_value
                        # the categorical variable already had a value set
                        else:
                            raise Exception("'{}' was already defined".format(variable))

                # if no binary flag was set for the categorical variable
                if value is None:
                    # if it is possible to have no value
                    if "none" in VALUES[variable]:
                        value = "none"
                    # if it is not possible to have no value but there is no value
                    else:
                        raise Exception("'{}' has no valid value".format(variable))

                # set the categorical variable flag in the mapped feature
                features[sample_index, metadata["value_to_index"][variable][value]] = 1.0

            # binary variable
            elif TYPES[variable] == "binary":
                value = read_binary(row[variable])
                assert value in [0, 1], "'{}' is not a valid value for '{}'".format(value, variable)
                features[sample_index, metadata["value_to_index"][variable][value]] = 1.0

            # unknown variable type
            else:
                raise Exception("Unknown variable type.")

        # label
        labels[sample_index] = row["shares"]

        # next row
        sample_index += 1

    # scale
    if scaler_path is not None:
        features, labels = scale_and_save_scaler(features, scaler_path, labels=labels)

    # add distributions to the metadata
    update_feature_distributions(metadata, features)

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

    options_parser.add_argument("--scaler", type=str,
                                help="Output scikit-learn MinMaxScaler in pickle format. Enables scaling to (0, 1).")

    options = options_parser.parse_args(args=args)

    online_news_popularity_transform(options.input,
                                     options.features,
                                     options.labels,
                                     options.metadata,
                                     options.scaler)


if __name__ == "__main__":
    main()
