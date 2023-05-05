import utils
import unittest


class TestUtils(unittest.TestCase):
    def test_clean_text(self):
        original_text = "Hello, World!"
        cleaned_text = utils.clean_text(original_text)
        self.assertEqual(cleaned_text, "hello world")

    def test_get_word_occurences(self):
        text = "hello world hello"
        word_occurences = utils.get_word_occurences(text)
        self.assertEqual(word_occurences, {"hello": 2, "world": 1})

    def test_combine_word_occurences(self):
        first = {"hello": 2, "world": 1}
        second = {"hello": 1, "world": 2, "foo": 3}
        combined = utils.combine_word_occurences(first, second)
        self.assertEqual(combined, {"hello": 3, "world": 3, "foo": 3})

    def test_get_word_occurences_parallel(self):
        texts = [
            "hello world hello",
            "hello world foo",
            "foo bar foo",
        ]

        word_occurences = utils.get_word_occurences_parallel(texts)
        self.assertEqual(word_occurences, {
            "hello": 3,
            "world": 2,
            "foo": 3,
            "bar": 1,
        })


if __name__ == "__main__":
    unittest.main()
