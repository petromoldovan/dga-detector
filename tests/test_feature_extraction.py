import unittest
import enchant
from models.feature_extraction import (
    get_vowel_to_consonant_ratio,
    get_real_words_ratio,
    calculate_percentage_of_repeating_chars,
    get_numbers_ratio,
    count_max_consecutive_characters_in_scope,
    VOWELS,
    CONSONANTS
)


class TestFeatureExtraction(unittest.TestCase):
    def test_get_vowel_to_consonant_ratio(self):
        self.assertEqual(get_vowel_to_consonant_ratio(''), 0, "Should be 0")
        self.assertEqual(get_vowel_to_consonant_ratio('ab'), 1, "Should be 1")
        self.assertEqual(get_vowel_to_consonant_ratio('abb'), 0.5, "Should be 0.5")
        self.assertEqual(get_vowel_to_consonant_ratio('eex'), 2, "Should be 2")

    def test_get_real_words_ratio(self):
        # EN dictionary
        dictionary = enchant.Dict("en_US")
        self.util_test_case_get_real_words_ratio(dictionary, 'bla1bla', [])
        self.util_test_case_get_real_words_ratio(dictionary, 'realword', ['real', 'word'])
        self.util_test_case_get_real_words_ratio(dictionary, 'realblawordbla', ['real', 'word'])
        self.util_test_case_get_real_words_ratio(dictionary, '33realblawordbla12', ['real', 'word'])
        self.util_test_case_get_real_words_ratio(dictionary, '33randomtrainblocksinkredrdbla12', ['random', 'train', 'blocks'])

    def test_calculate_percentage_of_repeating_chars(self):
        self.assertEqual(calculate_percentage_of_repeating_chars('aamm'), 1)
        self.assertEqual(calculate_percentage_of_repeating_chars('abcd'), 0)
        self.assertEqual(calculate_percentage_of_repeating_chars('ddddd'), 1)
        self.assertEqual(calculate_percentage_of_repeating_chars('abcgya'), 0.2)

    def test_get_numbers_ratio(self):
        self.assertEqual(get_numbers_ratio('aamm'), 0)
        self.assertEqual(get_numbers_ratio('1aamm'), 0.2)
        self.assertEqual(get_numbers_ratio('3333'), 1)

    def test_count_max_consecutive_characters_in_scope(self):
        self.assertEqual(count_max_consecutive_characters_in_scope('aaamm', VOWELS), 3)
        self.assertEqual(count_max_consecutive_characters_in_scope('aaaeeeemm', VOWELS), 7)
        self.assertEqual(count_max_consecutive_characters_in_scope('bvnmvbn', VOWELS), 0)
        self.assertEqual(count_max_consecutive_characters_in_scope('bvnmvbn', CONSONANTS), 7)
        self.assertEqual(count_max_consecutive_characters_in_scope('aaaeeeemm', CONSONANTS), 2)

    # ---------
    # Helpers--
    def util_test_case_get_real_words_ratio(self, dictionary, test_domain, exp_words):
        exp_ratio_of_real_words = len(''.join(exp_words)) / len(test_domain)
        ratio_of_real_words, ratio_of_longest_real_word = get_real_words_ratio(
            dictionary,
            test_domain
        )
        self.assertEqual(
            ratio_of_real_words,
            exp_ratio_of_real_words,
            "Should be " + str(exp_ratio_of_real_words)
        )


if __name__ == '__main__':
    unittest.main()
