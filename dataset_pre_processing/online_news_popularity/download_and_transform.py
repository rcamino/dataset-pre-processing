import wget
import zipfile

from dataset_pre_processing.online_news_popularity.transform import main as transform_main


def main():
    wget.download(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/00332/OnlineNewsPopularity.zip"
    )
    print()

    with zipfile.ZipFile("OnlineNewsPopularity.zip", "r") as zip_file:
        zip_file.extractall(".")

    transform_main(args=[
        "OnlineNewsPopularity/OnlineNewsPopularity.csv",
        "features.npy",
        "labels.npy",
        "metadata.json"
    ])


if __name__ == "__main__":
    main()
