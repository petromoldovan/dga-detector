from data.data import get_benign_domains
from os.path import exists
import json
import math

NGRAM_COUNT_FILE = 'data/ngram/ngram-count.json'
NGRAM_WEIGHTS_FILE = 'data/ngram/ngram-weights.json'

# each domain is broken down into sub strings for the following length
NGRAM_SUBSTRING_LENGTH = [3, 4, 5]


def get_ngram_dict_db():
    # calculate ngram if files are not there
    if not exists(NGRAM_COUNT_FILE):
        calculate_ngram_db()

    counts = {}
    with open(NGRAM_COUNT_FILE) as f:
        counts = json.load(f)

    weights = {}
    with open(NGRAM_WEIGHTS_FILE) as f:
        weights = json.load(f)

    return counts, weights


def calculate_ngram_db():
    # use only benign domains for ngram
    benign_domains, _ = get_benign_domains()     # get total: 930892

    total_substrings_count = 0
    ngram_count_dictionary = {}
    for domain in benign_domains:
        for n in NGRAM_SUBSTRING_LENGTH: # as in Woodbridge
            substrings = get_ngram_substrings(domain, n)
            # record each substring
            for substr in substrings:
                total_substrings_count += 1
                if substr in ngram_count_dictionary:
                    ngram_count_dictionary[substr] += 1
                else:
                    ngram_count_dictionary[substr] = 1

    # save file with count
    with open(NGRAM_COUNT_FILE, 'w') as fp:
        ngram_count_dictionary = sort_dict_by_value(ngram_count_dictionary)
        json.dump(ngram_count_dictionary, fp)

    # calculate weights
    # src: Zhao et al 2018
    # weight = log base 2 from (count substring occurances / ngram n)
    ngram_weights = {}
    for key in ngram_count_dictionary:
        count = ngram_count_dictionary[key]
        if len(key) >= count:
            continue

        weight = math.log2(count / len(key))
        ngram_weights[key] = weight

    # save file with weights
    with open(NGRAM_WEIGHTS_FILE, 'w') as fp:
        ngram_weights = sort_dict_by_value(ngram_weights)
        json.dump(ngram_weights, fp)


def get_ngram_substrings(domain, n):
    res = []
    start_idx = 0
    end_idx = n

    while end_idx <= len(domain):
        res.append(domain[start_idx:end_idx])
        # assign new end and start
        start_idx += 1
        end_idx += 1

    return res


def calculate_ngram_reputation_score(domain):
    _, weights_db = get_ngram_dict_db()
    score = 0

    for n in NGRAM_SUBSTRING_LENGTH:
        substrings = get_ngram_substrings(domain, n)
        # add score for each substring from weights DB
        for substr in substrings:
            if substr in weights_db:
                score += weights_db[substr]

    return score


def sort_dict_by_value(dictionary):
    return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=True)}


if __name__ == '__main__':
    calculate_ngram_db()
    # get_ngram_dict_db()
