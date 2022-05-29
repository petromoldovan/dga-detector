from data.data import get_data
from enchant.tokenize import get_tokenizer
import enchant
import math

# CONSTANTS
VOWELS = 'aeiou'
CONSONANTS = "bcdfghjklmnpqrstvwxyz"


def prepare_data_for_model():
    # TODO: remove
    raw_data, labels = get_data()

    # EN dictionary
    dictionary = enchant.Dict("en_US")

    features = []
    # feature extraction
    for domain in raw_data:
        item_features = []

        # SOURCE: Y. Li et al.: Machine Learning Framework for DGA-Based Malware Detection
        # 1. domain length
        domain_length = len(domain)
        item_features.append(domain_length)

        # 2. Ratio of real words
        ratio_of_real_words, ratio_of_longest_real_word = get_real_words_ratio(dictionary, domain, domain_length)
        item_features.append(ratio_of_real_words)
        # 3. Ration of the longest real word
        item_features.append(ratio_of_longest_real_word)

        # 4. Ratio of numeric characters
        numbers_ratio = get_numbers_ratio(domain)
        item_features.append(numbers_ratio)

        # 5. Pronounceability score???

        # SOURCE: Almashhadani
        # 6. Max consecutive vowels
        item_features.append(count_max_consecutive_characters_in_scope(domain, VOWELS))

        # 7. Max consecutive consonants
        item_features.append(count_max_consecutive_characters_in_scope(domain, CONSONANTS))

        # 8. Shanon entropy
        item_features.append(shannon_entropy(domain))

        # Source: Woodbridge
        # 9. n-gram normality score
        # 10. vowel to consonant ratio
        #

        # push to resulting array
        features.append(item_features)

    return raw_data, labels, features


def get_numbers_ratio(domain):
    count = 0
    for letter in domain:
        if letter.isdigit():
            count += 1

    return count / len(domain)


def get_real_words_ratio(dictionary, domain, domain_length):
    # length of real words devided by domain length
    real_words = []
    start_idx = 0
    while start_idx < domain_length:
        end_idx = domain_length
        found = False
        while start_idx < end_idx:
            substring = domain[start_idx:end_idx]

            # TODO: consider only words that are at least 3 chars. Experiment with it!!! try 4.
            if len(substring) > 2 and dictionary.check(substring):
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


if __name__ == '__main__':
    prepare_data_for_model()
