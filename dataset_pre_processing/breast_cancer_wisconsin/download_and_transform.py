import wget

from dataset_pre_processing.breast_cancer_wisconsin.transform import main as transform_main


def main():
    wget.download(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/breast-cancer-wisconsin.data"
    )
    print()

    transform_main(args=[
        "breast-cancer-wisconsin.data",
        "features.npy",
        "labels.npy",
        "metadata.json"
    ])


if __name__ == "__main__":
    main()
