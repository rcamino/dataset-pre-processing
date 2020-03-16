import argparse
import os
import wget
import zipfile

from dataset_pre_processing.uci.online_news_popularity.transform import main as transform_main


def main():
    options_parser = argparse.ArgumentParser(description="Download the data and transform with default values.")

    options_parser.add_argument("--directory", type=str, help="Output directory.")

    options = options_parser.parse_args()

    directory = options.directory
    if directory is None:
        directory = os.getcwd()

    compressed_path = os.path.join(directory, "OnlineNewsPopularity.zip")
    file_name = "OnlineNewsPopularity.csv"
    subdirectory = os.path.join(directory, "OnlineNewsPopularity")
    file_path = os.path.join(directory, file_name)

    # download the zip
    wget.download(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/00332/OnlineNewsPopularity.zip",
        compressed_path
    )
    print()

    # extract the file from the zip
    with zipfile.ZipFile(compressed_path, "r") as zip_file:
        zip_file.extract("OnlineNewsPopularity/OnlineNewsPopularity.csv", directory)

    # move out the file from the annoying subdirectory
    os.rename(os.path.join(subdirectory, file_name), file_path)
    # remove the empty subdirectory
    os.rmdir(subdirectory)
    # remove the zip
    os.remove(compressed_path)

    transform_main(args=[
        file_path,
        os.path.join("features.npy"),
        os.path.join("labels.npy"),
        os.path.join("metadata.json"),
        "--scaler=" + os.path.join(directory, "scaler.pickle")
    ])


if __name__ == "__main__":
    main()
