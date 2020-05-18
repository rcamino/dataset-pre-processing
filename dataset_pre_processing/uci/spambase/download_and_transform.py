import argparse
import os
import wget

from dataset_pre_processing.uci.spambase.transform import main as transform_main


def main():
    options_parser = argparse.ArgumentParser(description="Download the data and transform with default values.")

    options_parser.add_argument("--directory", type=str, help="Output directory.")

    options = options_parser.parse_args()

    directory = options.directory
    if directory is None:
        directory = os.getcwd()

    file_path = os.path.join(directory, "spambase.data")

    wget.download(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/spambase/spambase.data",
        file_path
    )
    print()

    transform_main(args=[
        file_path,
        os.path.join(directory, "features.npy"),
        os.path.join(directory, "labels.npy"),
        os.path.join(directory, "metadata.json"),
        "--scaler=" + os.path.join(directory, "scaler.pickle")
    ])


if __name__ == "__main__":
    main()
