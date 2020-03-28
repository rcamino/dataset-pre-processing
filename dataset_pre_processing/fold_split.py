import argparse
import os

import numpy as np

from sklearn.model_selection import KFold, StratifiedKFold


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

    options = options_parser.parse_args()

    features = np.load(options.features)

    if options.labels is None:
        labels = None
    else:
        labels = np.load(options.labels)

    if options.labels is not None and options.stratify:
        fold_generator = StratifiedKFold(n_splits=options.folds, shuffle=options.shuffle).split(features, labels)
    else:
        fold_generator = KFold(n_splits=options.folds, shuffle=options.shuffle).split(features)
        
    for fold_number, (train_index, test_index) in enumerate(fold_generator):
        fold_number += 1  # index the folds from 1 to N inclusive

        train_features, test_features = features[train_index, :], features[test_index, :]
        template = os.path.join(options.output_directory, options.features_template)

        np.save(template.format(name="train", number=fold_number, total=options.folds), train_features)
        np.save(template.format(name="test", number=fold_number, total=options.folds), test_features)

        if options.labels is not None:
            train_labels, test_labels = labels[train_index], labels[test_index]
            template = os.path.join(options.output_directory, options.labels_template)

            np.save(template.format(name="train", number=fold_number, total=options.folds), train_labels)
            np.save(template.format(name="test", number=fold_number, total=options.folds), test_labels)


if __name__ == "__main__":
    main()
