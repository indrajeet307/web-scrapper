import unittest

import read_html as rh


class TestReadHtml(unittest.TestCase):
    def test_is_externla_link(self):

        self.assertFalse(rh.is_external_link("http://www.test.com/about", "www.test.com"))
        self.assertTrue(rh.is_external_link("http://www.test.com/about", "www.test1.com"))

    def test_get_data(self):
        test_html = """
        <html>
        <body>
        <a href="http://www.test.com"/>
        <a href="http://www.test2.com"/>
        <div>test para</div></body>
        </html>
        """

        uni, bi, links = rh.parse_page_data(test_html, "www.test.com")

        self.assertEqual(list(uni.keys()), ["test", "para"])
        self.assertEqual(list(bi.keys()), ["test para"])
        self.assertEqual(links, {"http://www.test.com"})

    def test_generate_ngram(self):
        word_list = "a b c d".split()

        one_grams = rh.generate_ngrams(word_list, 1)
        bigrams = rh.generate_ngrams(word_list, 2)

        self.assertEqual(one_grams, word_list)
        self.assertEqual(bigrams, ["a b", "b c", "c d"])
