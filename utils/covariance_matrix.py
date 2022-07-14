import numpy as np
from models.feature_extraction import get_data_for_model

cov_matrix = []

def build_cov_matrix():
    _, features = get_data_for_model()
    feat_count = len(features[0])
    main_idx = 0
    while main_idx < feat_count:
        try:
            cov_matrix[main_idx]
        except IndexError:
            cov_matrix.append([])

        test_single_feature(features, main_idx)
        main_idx += 1

    print("cov_matrix", cov_matrix)


def test_single_feature(features, feat_idx):
    # print("++++++++++++++++++++++++++")
    feat_count = len(features[0])

    # get main feature
    feat_main = []
    for item in features:
        feat_main.append(item[feat_idx])

    idx_dep = 0
    while idx_dep < feat_count:
        dependant_feat = []
        for item in features:
            dependant_feat.append(item[idx_dep])

        # Pearson's correlation coefficient
        pcc = np.corrcoef(feat_main, dependant_feat)
        correlation = round(pcc[0][1], 2)

        cov_matrix[feat_idx].append(correlation)

        idx_dep += 1


if __name__ == '__main__':
    build_cov_matrix()


# [
#     [1.0, -0.05, -0.13, 0.35, 0.26, 0.77, -0.1, 0.28, 0.57],
#     [-0.05, 1.0, 0.92, -0.29, -0.27, 0.05, 0.18, 0.69, 0.01],
#     [-0.13, 0.92, 1.0, -0.28, -0.29, -0.03, 0.19, 0.55, -0.06],
#     [0.35, -0.29, -0.28, 1.0, -0.2, 0.15, -0.06, -0.33, 0.23],
#     [0.26, -0.27, -0.29, -0.2, 1.0, 0.34, -0.52, -0.14, 0.09],
#     [0.77, 0.05, -0.03, 0.15, 0.34, 1.0, -0.17, 0.31, 0.13],
#     [-0.1, 0.18, 0.19, -0.06, -0.52, -0.17, 1.0, 0.2, 0.04],
#     [0.28, 0.69, 0.55, -0.33, -0.14, 0.31, 0.2, 1.0, 0.25],
#     [0.57, 0.01, -0.06, 0.23, 0.09, 0.13, 0.04, 0.25, 1.0]
# ]
