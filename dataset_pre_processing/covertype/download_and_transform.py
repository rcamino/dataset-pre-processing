import gzip
import shutil
import wget

from dataset_pre_processing.covertype.transform import main as transform_main


def main():
    wget.download("https://archive.ics.uci.edu/ml/machine-learning-databases/covtype/covtype.data.gz")
    print()

    with gzip.open("covtype.data.gz", "rb") as input_file:
        with open("covtype.data", "wb") as output_file:
            shutil.copyfileobj(input_file, output_file)

    transform_main(args=[
        "covtype.data",
        "features.npy",
        "labels.npy",
        "metadata.json"
    ])


if __name__ == "__main__":
    main()
