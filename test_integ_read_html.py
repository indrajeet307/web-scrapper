import unittest

import read_html as rh


class IntegTests(unittest.TestCase):
    def test_sequential_code(self):
        """TODO"""
        unigrams, bigrams = rh.depth_traversal("http://localhost:8000/", 4)
        print(unigrams, bigrams, sep="\n\n")

    def test_concurrent_code(self):
        """TODO"""
        unigrams, bigrams = rh.depth_traversal_with_concurrency("http://localhost:8000/", 4, 10)
        print(unigrams, bigrams, sep="\n\n")
        self.fail()
