import argparse

import numpy as np

from sklearn.model_selection import train_test_split


def compute_size_of_each_side(features, one_side_value):
    # if the size is a ratio
    if 0 < one_side_value < 1:
        size_one_side = one_side_value
        size_other_side = 1.0 - one_side_value
    # if the size is not a ratio it must be a valid amount of samples
    elif 0 < one_side_value < features.shape[0]:
        size_one_side = int(one_side_value)
        size_other_side = features.shape[0] - size_one_side
    # if the size is invalid
    else:
        raise Exception("Invalid size.")

    return size_one_side, size_other_side


def main():
    options_parser = argparse.ArgumentParser(description="Split features file into train and test files.")

    options_parser.add_argument("features", type=str, help="Input features in numpy array format.")
    options_parser.add_argument("train_size", type=float, help="Number or proportion of samples for the train part.")
    options_parser.add_argument("train_features", type=str, help="Output train features in numpy array format.")
    options_parser.add_argument("test_features", type=str, help="Output test features in numpy array format.")

    options_parser.add_argument("--labels", type=str, help="Input labels in numpy array format.")
    options_parser.add_argument("--train_labels", type=str, help="Output train labels in numpy array format.")
    options_parser.add_argument("--test_labels", type=str, help="Output test labels in numpy array format.")

    options_parser.add_argument("--shuffle", default=False, action="store_true",
                                help="Shuffle samples before the split.")

    options_parser.add_argument("--stratify", default=False, action="store_true",
                                help="Split preserving class proportions (only valid with labels).")

    options = options_parser.parse_args()

    # load the features
    features = np.load(options.features)

    # compute train and test size
    train_size, test_size = compute_size_of_each_side(features, options.train_size)

    # without labels
    if options.labels is None:
        # split
        train_features, test_features = train_test_split(features,
                                                         train_size=train_size,
                                                         test_size=test_size,
                                                         shuffle=options.shuffle)

        # save the features
        np.save(options.train_features, train_features)
        np.save(options.test_features, test_features)

    # with labels
    else:
        # load the labels
        labels = np.load(options.labels)

        # split with stratification
        if options.stratify:
            train_features, test_features, train_labels, test_labels = train_test_split(features,
                                                                                        labels,
                                                                                        train_size=train_size,
                                                                                        test_size=test_size,
                                                                                        shuffle=True,  # mandatory
                                                                                        stratify=labels)
        # split without stratification
        else:
            train_features, test_features, train_labels, test_labels = train_test_split(features,
                                                                                        labels,
                                                                                        train_size=train_size,
                                                                                        test_size=test_size,
                                                                                        shuffle=options.shuffle)

        # save the features and labels
        np.save(options.train_features, train_features)
        np.save(options.test_features, test_features)
        np.save(options.train_labels, train_labels)
        np.save(options.test_labels, test_labels)


if __name__ == "__main__":
    main()
