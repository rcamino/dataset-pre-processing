import pickle

import numpy as np

from sklearn.preprocessing import MinMaxScaler


def _concatenate_and_split_if_needed(features, action, labels=None):
    if labels is None:
        data = features
    else:
        data = np.concatenate((features, labels.reshape(-1, 1)), axis=1)

    data = action(data)

    if labels is None:
        return data
    else:
        return data[:, :-1], data[:, -1]


def scale_and_save_scaler(features, scaler_path, labels=None, feature_range=(0, 1)):
    def action(data):
        scaler = MinMaxScaler(feature_range=feature_range, copy=True)
        data = scaler.fit_transform(data)

        with open(scaler_path, "wb") as scaler_file:
            pickle.dump(scaler, scaler_file)

        return data

    return _concatenate_and_split_if_needed(features, action, labels=labels)


def scale(features, scaler_path, labels=None):
    def action(data):
        with open(scaler_path, "rb") as scaler_file:
            scaler = pickle.load(scaler_file)

        return scaler.transform(data)

    return _concatenate_and_split_if_needed(features, action, labels=labels)


def inverse_scale(features, scaler_path, labels=None):
    def action(data):
        with open(scaler_path, "rb") as scaler_file:
            scaler = pickle.load(scaler_file)

        return scaler.inverse_transform(data)

    return _concatenate_and_split_if_needed(features, action, labels=labels)
