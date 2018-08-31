import wget


from dataset_pre_processing.adult.transform import main as transform_main


def main():
    wget.download("http://mlr.cs.umass.edu/ml/machine-learning-databases/adult/adult.data")
    print()
    wget.download("http://mlr.cs.umass.edu/ml/machine-learning-databases/adult/adult.test")
    print()

    transform_main(args=[
        "adult.data",
        "adult.test",
        "features-train.npy",
        "features-test.npy",
        "labels-train.npy",
        "labels-test.npy",
        "metadata.json",
        "--ignore_missing"
    ])


if __name__ == "__main__":
    main()
