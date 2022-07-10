import json
from models.feature_extraction import DATA_LABELS_FILE, DATA_FEATURES_FILE

# 0 - domain length
# 4 - max consecutive consonants
# 5 - Shanon entropy
# 7 - N-Gram
def get_domain_length_distribution(feature_id, round_digits = 2):
    labels = []
    try:
        with open(DATA_LABELS_FILE) as f:
            labels = json.load(f)
    except:
        pass

    features = []
    try:
        with open(DATA_FEATURES_FILE) as f:
            features = json.load(f)
    except:
        pass

    dga_map = {}
    benign_map = {}
    for i in range(len(features)):
        feat = features[i][feature_id]
        feat = round(feat, round_digits)
        if labels[i] == 'benign':
            if feat in benign_map:
                benign_map[feat] = benign_map[feat] + 1
            else:
                benign_map[feat] = 1
        else:
            if feat in dga_map:
                dga_map[feat] = dga_map[feat] + 1
            else:
                dga_map[feat] = 1

    print("benign--------------")
    for key in benign_map:
        print("key ", key, " value: ", benign_map[key])

    # print("DGA--------------")
    for key in dga_map:
        print("key ", key, " value: ", dga_map[key])

    return

if __name__ == '__main__':
    get_domain_length_distribution(7, 0)
