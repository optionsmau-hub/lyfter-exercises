import unittest
from functions import (
    sum_list,
    reverse_string,
    count_upper_lower,
    sort_hyphenated_words,
    filter_primes,
)


class TestSumList(unittest.TestCase):
    """Exercise 3: sum of all numbers in a list."""

    def test_example_from_statement(self):
        self.assertEqual(sum_list([4, 6, 2, 29]), 41)

    def test_list_with_negative_numbers(self):
        self.assertEqual(sum_list([-5, 10, -2, 3]), 6)

    def test_list_with_single_element(self):
        self.assertEqual(sum_list([7]), 7)


class TestReverseString(unittest.TestCase):
    """Exercise 4: reverse a string."""

    def test_example_from_statement(self):
        self.assertEqual(reverse_string("Hello world"), "dlrow olleH")

    def test_single_word(self):
        self.assertEqual(reverse_string("Python"), "nohtyP")

    def test_palindrome_stays_equal(self):
        self.assertEqual(reverse_string("ana"), "ana")


class TestCountUpperLower(unittest.TestCase):
    """Exercise 5: count uppercase and lowercase letters in a string."""

    def test_example_from_statement(self):
        self.assertEqual(
            count_upper_lower("I love Nación Sushi"),
            "There's 3 upper cases and 13 lower cases",
        )

    def test_all_uppercase(self):
        self.assertEqual(
            count_upper_lower("ABC"),
            "There's 3 upper cases and 0 lower cases",
        )

    def test_all_lowercase(self):
        self.assertEqual(
            count_upper_lower("abc"),
            "There's 0 upper cases and 3 lower cases",
        )


class TestSortHyphenatedWords(unittest.TestCase):
    """Exercise 6: sort hyphen-separated words alphabetically."""

    def test_example_from_statement(self):
        self.assertEqual(
            sort_hyphenated_words(
                "python-variable-function-computer-monitor"
            ),
            "computer-function-monitor-python-variable",
        )

    def test_two_words(self):
        self.assertEqual(sort_hyphenated_words("banana-apple"), "apple-banana")

    def test_already_sorted_words(self):
        self.assertEqual(sort_hyphenated_words("apple-banana-cherry"), "apple-banana-cherry")


class TestFilterPrimes(unittest.TestCase):
    """Exercise 7: filter prime numbers out of a list."""

    def test_example_from_statement(self):
        self.assertEqual(filter_primes([1, 4, 6, 7, 13, 9, 67]), [7, 13, 67])

    def test_list_with_no_primes(self):
        self.assertEqual(filter_primes([1, 4, 6, 8, 9, 10]), [])

    def test_list_with_all_primes(self):
        self.assertEqual(filter_primes([2, 3, 5, 7, 11]), [2, 3, 5, 7, 11])


if __name__ == "__main__":
    unittest.main()
