import unittest
from data.ngram.ngram import (
    get_ngram_substrings,
)


class TestFeatureExtraction(unittest.TestCase):
    def test_get_ngram_substrings(self):
        self.assertEqual(get_ngram_substrings('amazonprime', 3), ['ama', 'maz', 'azo', 'zon', 'onp', 'npr', 'pri', 'rim', 'ime'])
        self.assertEqual(get_ngram_substrings('best', 3), ['bes', 'est'])


if __name__ == '__main__':
    unittest.main()
