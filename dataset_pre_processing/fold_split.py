import argparse
import os

import numpy as np

from sklearn.model_selection import KFold, StratifiedKFold, train_test_split

from dataset_pre_processing.train_test_split import compute_size_of_each_side


def main():
    options_parser = argparse.ArgumentParser(description="Split features file into several train and test files.")

    options_parser.add_argument("features", type=str, help="Input features in numpy array format.")
    options_parser.add_argument("folds", type=int, help="Number of folds.")
    options_parser.add_argument("output_directory", type=str, help="Output directory path for the folds.")

    options_parser.add_argument("features_template", type=str,
                                help="Output features file name template. Variables: name, number, total.")

    options_parser.add_argument("--labels", type=str, help="Input labels in numpy array format.")

    options_parser.add_argument("--labels_template", type=str,
                                help="Output labels file name template. Variables: name, number, total.")

    options_parser.add_argument("--shuffle", default=False, action="store_true",
                                help="Shuffle samples before the split.")

    options_parser.add_argument("--stratify", default=False, action="store_true",
                                help="Split preserving class proportions (only valid with labels).")

    options_parser.add_argument("--validation", type=float,
                                help="Number or proportion of samples from the train set for the validation set.")

    options = options_parser.parse_args()

    features = np.load(options.features)

    features_template = os.path.join(options.output_directory, options.features_template)
    
    # prepare labels if used
    labels_used = options.labels is not None
    if labels_used:
        labels = np.load(options.labels)
        labels_template = os.path.join(options.output_directory, options.labels_template)
    else:
        labels = None
        labels_template = None

    # create folds
    if labels_used and options.stratify:
        fold_generator = StratifiedKFold(n_splits=options.folds, shuffle=options.shuffle).split(features, labels)
    else:
        fold_generator = KFold(n_splits=options.folds, shuffle=options.shuffle).split(features)

    # iterate folds
    for fold, (train_index, test_index) in enumerate(fold_generator, start=1):
        # use a part of the train set as validation (must be done before using the train set)
        if options.validation is not None:
            # compute val and train size
            val_size, train_size = compute_size_of_each_side(train_index, options.validation)
            
            # if labels are used with stratification
            if labels_used and options.stratify:
                # split the train index into train and validation index
                train_index, val_index = train_test_split(train_index,
                                                          train_size=train_size,
                                                          test_size=val_size,
                                                          shuffle=True,  # mandatory
                                                          stratify=labels[train_index])

            # if labels are not used or if they are used but without stratification
            else:
                # split the train index into train and validation index
                train_index, val_index = train_test_split(train_index,
                                                          train_size=train_size,
                                                          test_size=val_size,
                                                          shuffle=options.shuffle)

            # now use the validation index
            # the train index will be used normally afterwards
            np.save(features_template.format(name="val", fold=fold, total=options.folds), features[val_index, :])
            if labels_used:
                np.save(labels_template.format(name="val", fold=fold, total=options.folds), labels[val_index])

        # now continue saving the train and test sets
        np.save(features_template.format(name="train", fold=fold, total=options.folds), features[train_index, :])
        np.save(features_template.format(name="test", fold=fold, total=options.folds), features[test_index, :])

        # if labels are used
        if labels_used:
            np.save(labels_template.format(name="train", fold=fold, total=options.folds), labels[train_index])
            np.save(labels_template.format(name="test", fold=fold, total=options.folds), labels[test_index])


if __name__ == "__main__":
    main()
