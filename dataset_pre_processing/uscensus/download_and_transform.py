import wget

from dataset_pre_processing.uscensus.transform import main as transform_main


def main():
    wget.download(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/census1990-mld/USCensus1990.data.txt"
    )
    print()

    transform_main(args=[
        "USCensus1990.data.txt",
        "features.npz",
        "metadata.json"
    ])


if __name__ == "__main__":
    main()
