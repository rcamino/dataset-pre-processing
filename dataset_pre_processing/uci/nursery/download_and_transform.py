import argparse
import os
import wget

from dataset_pre_processing.uci.nursery.transform import main as transform_main


def main():
    options_parser = argparse.ArgumentParser(description="Download the data and transform with default values.")

    options_parser.add_argument("--directory", type=str, help="Output directory.")

    options = options_parser.parse_args()

    directory = options.directory
    if directory is None:
        directory = os.getcwd()

    file_path = os.path.join(directory, "nursery.data")

    wget.download(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/nursery/nursery.data",
        file_path
    )
    print()

    transform_main(args=[
        file_path,
        os.path.join("features.npy"),
        os.path.join("labels.npy"),
        os.path.join("metadata.json"),
    ])


if __name__ == "__main__":
    main()
