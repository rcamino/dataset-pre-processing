import wget

from dataset_pre_processing.spambase.transform import main as transform_main


def main():
    wget.download(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/spambase/spambase.data"
    )
    print()

    transform_main(args=[
        "spambase.data",
        "features.npy",
        "labels.npy",
        "metadata.json"
    ])


if __name__ == "__main__":
    main()
