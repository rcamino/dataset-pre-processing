import argparse
import gzip
import os
import shutil
import wget

from dataset_pre_processing.uci.covertype.transform import main as transform_main


def main():
    options_parser = argparse.ArgumentParser(description="Download the data and transform with default values.")

    options_parser.add_argument("--directory", type=str, help="Output directory.")

    options = options_parser.parse_args()

    directory = options.directory
    if directory is None:
        directory = os.getcwd()

    compressed_path = os.path.join(directory, "covtype.data.gz")
    data_path = os.path.join(directory, "covtype.data")

    wget.download("https://archive.ics.uci.edu/ml/machine-learning-databases/covtype/covtype.data.gz", compressed_path)
    print()

    with gzip.open(compressed_path, "rb") as compressed_file:
        with open(data_path, "wb") as data_file:
            shutil.copyfileobj(compressed_file, data_file)

    transform_main(args=[
        data_path,
        os.path.join(directory, "features.npy"),
        os.path.join(directory, "labels.npy"),
        os.path.join(directory, "metadata.json"),
        "--scaler=" + os.path.join(directory, "scaler.pickle")
    ])


if __name__ == "__main__":
    main()
