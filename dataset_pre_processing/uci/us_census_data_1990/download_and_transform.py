import argparse
import os
import wget

from dataset_pre_processing.uci.us_census_data_1990.transform import main as transform_main


def main():
    options_parser = argparse.ArgumentParser(description="Download the data and transform with default values.")

    options_parser.add_argument("--directory", type=str, help="Output directory.")

    options = options_parser.parse_args()

    directory = options.directory
    if directory is None:
        directory = os.getcwd()

    file_path = os.path.join(directory, "USCensus1990.data.txt")

    wget.download(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/census1990-mld/USCensus1990.data.txt",
        file_path
    )
    print()

    transform_main(args=[
        file_path,
        os.path.join(directory, "features.npz"),
        os.path.join(directory, "metadata.json")
    ])


if __name__ == "__main__":
    main()
