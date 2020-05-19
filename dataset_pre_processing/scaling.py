import pickle

from sklearn.preprocessing import MinMaxScaler


def scale_and_save_scaler(features, scaler_path, feature_range=(0, 1)):
    scaler = MinMaxScaler(feature_range=feature_range, copy=True)
    features = scaler.fit_transform(features)

    with open(scaler_path, "wb") as scaler_file:
        pickle.dump(scaler, scaler_file)

    return features
