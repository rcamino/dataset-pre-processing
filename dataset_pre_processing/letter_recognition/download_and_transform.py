import wget

from dataset_pre_processing.letter_recognition.transform import main as transform_main


def main():
    wget.download(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/letter-recognition/letter-recognition.data"
    )
    print()

    transform_main(args=[
        "letter-recognition.data",
        "features.npy",
        "labels.npy",
        "metadata.json"
    ])


if __name__ == "__main__":
    main()
