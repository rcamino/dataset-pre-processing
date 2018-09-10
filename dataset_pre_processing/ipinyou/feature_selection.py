from __future__ import print_function

import argparse
import os

import pandas as pd


MODES = ["train", "test"]

FILTERED_FIELDS = [
    "useragent",
    "region",
    "city",
    "adexchange",
    "slotwidth",
    "slotheight",
    "slotvisibility",
    "creative"
]


def ipinyou_feature_selection(directory, filtered_field_names=None):
    campaigns = sorted([subdirectory for subdirectory in os.listdir(directory) if subdirectory != "all"])

    for campaign in campaigns:
        print("Campaign:", campaign)
        ipinyou_feature_selection_campaign(directory, campaign, filtered_field_names)


def ipinyou_feature_selection_campaign(directory, campaign, filtered_field_names=None):
    if filtered_field_names is None:
        filtered_field_names = FILTERED_FIELDS

    for mode in MODES:
        print("Mode:", mode)

        filtered_field_names = set(filtered_field_names)
        filtered_field_names.add("click")
        filtered_field_names.add("payprice")
        filtered_field_names = sorted(filtered_field_names)

        input_path = os.path.join(directory, str(campaign), "{}.log.txt".format(mode))
        output_path = os.path.join(directory, str(campaign), "{}-filtered.log.txt".format(mode))

        df = pd.read_csv(input_path, delimiter="\t")
        df = df.sort_values(by=['timestamp'])
        df = df[filtered_field_names]
        df.to_csv(output_path, sep="\t", index=False)


def main():
    options_parser = argparse.ArgumentParser(
        description="Select columns from iPinYou train and test text data and save into a new text one."
    )

    options_parser.add_argument(
        "directory",
        type=str,
        help="iPinYou data directory containing train.log.txt and test.log.txt"
    )

    options_parser.add_argument(
        "--features",
        type=str,
        default=",".join(FILTERED_FIELDS),
        help="Column names separated by commas."
    )

    options = options_parser.parse_args()

    ipinyou_feature_selection(options.directory, options.features.split(","))

if __name__ == "__main__":
    main()
