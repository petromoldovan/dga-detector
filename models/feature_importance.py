import numpy as np
from models.feature_extraction import get_data_for_model


def check_feature_importance():
    labels, features = get_data_for_model()

    labels_binary = [0 if lab == 'benign' else 1 for lab in labels]

    feature_importance = []

    feat_count = len(features[0])
    idx = 0
    while idx < feat_count:
        feat = []
        for item in features:
            feat.append(item[idx])

        # Pearson's correlation coefficient
        pcc = np.corrcoef(feat, labels_binary)
        correlation = round(pcc[0][1], 2)
        feature_importance.append(correlation)

        idx += 1

    print ("Tested features:", len(feature_importance))
    print ("feature importance:", feature_importance)


if __name__ == '__main__':
    check_feature_importance()
