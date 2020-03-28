import argparse

import numpy as np

from sklearn.model_selection import train_test_split


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

    # if the train size is a ratio
    if 0 < options.train_size < 1:
        train_size = options.train_size
        test_size = 1.0 - options.train_size  # a warning is thrown if not specified
    # if the train size is not a ratio it must be a valid number
    elif options.train_size < features.shape[0]:
        train_size = int(options.train_size)
        test_size = features.shape[0] - train_size  # a warning is thrown if not specified
    # if the train size is invalid
    else:
        raise Exception("Invalid train size.")

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
