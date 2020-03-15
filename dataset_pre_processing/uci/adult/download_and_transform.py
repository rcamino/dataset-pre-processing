import argparse
import os
import wget


from dataset_pre_processing.uci.adult.transform import main as transform_main


def main():
    options_parser = argparse.ArgumentParser(description="Download the data and transform with default values.")

    options_parser.add_argument("--directory", type=str, help="Output directory.")

    options = options_parser.parse_args()

    directory = options.directory
    if directory is None:
        directory = os.getcwd()

    train_path = os.path.join(directory, "adult.data")
    test_path = os.path.join(directory, "adult.data")

    wget.download("http://mlr.cs.umass.edu/ml/machine-learning-databases/adult/adult.data", train_path)
    print()

    wget.download("http://mlr.cs.umass.edu/ml/machine-learning-databases/adult/adult.test", test_path)
    print()

    transform_main(args=[
        train_path,
        test_path,
        os.path.join(directory, "features.npy"),
        os.path.join(directory, "labels.npy"),
        os.path.join(directory, "metadata.json"),
        "--ignore_missing",
        "--scaler=" + os.path.join(directory, "scaler.pickle")
    ])


if __name__ == "__main__":
    main()
