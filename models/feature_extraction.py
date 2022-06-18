import enchant
import math
import json

from data.data import get_data
from data.ngram.ngram import calculate_ngram_reputation_score, get_ngram_dict_db

# CONSTANTS
VOWELS = 'aeiou'
CONSONANTS = "bcdfghjklmnpqrstvwxyz"

# DATA_FEATURES_FILE = 'data/db_features/features.json'
# DATA_LABELS_FILE = 'data/db_features/labels.json'
DATA_FEATURES_FILE = 'data/db_features/features-600k.json'
DATA_LABELS_FILE = 'data/db_features/labels-600k.json'

def get_data_for_model():
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

    if len(labels) > 0 and len(features) > 0:
        print("Reading data from file:")
        print ("len(labels)", len(labels))
        print ("len(features)", len(features))
        return labels, features

    # if no data available recalculate again
    labels, features = prepare_data_for_model()

    # save data
    with open(DATA_LABELS_FILE, 'w') as fp:
        fp.truncate(0)
        json.dump(labels, fp)

    with open(DATA_FEATURES_FILE, 'w') as fp:
        fp.truncate(0)
        json.dump(features, fp)

    return labels, features


def prepare_data_for_model():
    # TODO: remove
    raw_data, labels = get_data()

    # EN dictionary
    dictionary = enchant.Dict("en_US")

    # NGram DB. Initialize once to speed up feature extraction.
    _, weights_db = get_ngram_dict_db()

    # feature extraction
    features = []
    for domain in raw_data:
        if not domain or domain == "":
            continue

        item_features = []

        # print ("domain", domain)

        # SOURCE: Y. Li et al.: Machine Learning Framework for DGA-Based Malware Detection
        # 1. domain length
        domain_length = len(domain)
        item_features.append(domain_length)

        # 2. Ratio of real words
        ratio_of_real_words, ratio_of_longest_real_word = get_real_words_ratio(dictionary, domain)
        item_features.append(ratio_of_real_words)
        # 3. Ratio of the longest real word
        item_features.append(ratio_of_longest_real_word)

        # 4. Ratio of numeric characters
        numbers_ratio = get_numbers_ratio(domain)
        item_features.append(numbers_ratio)

        # SOURCE: Almashhadani
        # 5. Max consecutive vowels
        # item_features.append(count_max_consecutive_characters_in_scope(domain, VOWELS))

        # 6. Max consecutive consonants
        item_features.append(count_max_consecutive_characters_in_scope(domain, CONSONANTS))

        # 7. Shanon entropy
        item_features.append(shannon_entropy(domain))

        # Source: Woodbridge
        # 8. vowel to consonant ratio
        item_features.append(get_vowel_to_consonant_ratio(domain))

        # 9. n-gram normality score
        item_features.append(calculate_ngram_reputation_score(domain, weights_db))

        # own metric
        # 10. percentage of repeating chars
        item_features.append(calculate_percentage_of_repeating_chars(domain))

        # push to resulting array
        features.append(item_features)

    return labels, features


def get_numbers_ratio(domain):
    count = 0
    for letter in domain:
        if letter.isdigit():
            count += 1

    return count / len(domain)


def get_real_words_ratio(dictionary, domain):
    # length of real words devided by domain length
    real_words = []
    start_idx = 0
    domain_length = len(domain)
    while start_idx < domain_length:
        end_idx = domain_length
        found = False
        while start_idx < end_idx:
            substring = domain[start_idx:end_idx]

            # TODO: consider only words that are at least 4 chars.
            if len(substring) > 3 and dictionary.check(substring):
                real_words.append(substring)
                start_idx = end_idx
                found = True
                break
            else:
                end_idx -= 1

        if not found:
            start_idx += 1

    all_words_length = len(''.join(real_words))
    # print("========")
    # print("domain", domain)
    # print("real_words", real_words)
    # print("ratio", all_words_length / domain_length)

    ratio_of_real_words = all_words_length / domain_length

    ratio_of_longest_real_word = 0
    if len(real_words) > 0:
        ratio_of_longest_real_word = len(max(real_words, key=len)) / domain_length

    return ratio_of_real_words, ratio_of_longest_real_word


def shannon_entropy(string):
    # calculate probability of chars in the string
    probability = [ float(string.count(c)) / len(string) for c in dict.fromkeys(list(string)) ]

    # calculate the entropy
    entropy = - sum([ p * math.log(p) / math.log(2.0) for p in probability ])

    return entropy


def count_max_consecutive_characters_in_scope(domain, scope):
    results = [0]

    for letter in domain:
        if letter in scope:
            # update last item
            results[-1] += 1
        else:
            # add new last item
            results.append(0)

    return max(results)


def get_vowel_to_consonant_ratio(domain):
    vowels_count = 0
    consonants_count = 0

    for letter in domain:
        if letter in VOWELS:
            vowels_count += 1
        elif letter in CONSONANTS:
            consonants_count += 1

    if consonants_count > 0:
        return vowels_count / consonants_count

    return 0


def calculate_percentage_of_repeating_chars(domain):
    chars = {}

    # get map of unique chars
    for char in domain:
        if char in chars:
            chars[char] += 1

        else:
            chars[char] = 1

    repeating_chars = 0
    for key in chars:
        if chars[key] > 1:
            repeating_chars += 1

    return repeating_chars / len(chars)


if __name__ == '__main__':
    get_data_for_model()
