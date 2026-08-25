import unittest
import random
from bubble_sort import bubble_sort


class TestBubbleSort(unittest.TestCase):

    def test_small_list(self):
        """Works with a small list."""
        result = bubble_sort([5, 3, 8, 1, 9])
        self.assertEqual(result, [1, 3, 5, 8, 9])

    def test_large_list(self):
        """Works with a large list (more than 100 elements)."""
        large_list = [random.randint(0, 10000) for _ in range(150)]
        expected = sorted(large_list.copy())
        result = bubble_sort(large_list)
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 150)

    def test_empty_list(self):
        """Works with an empty list."""
        result = bubble_sort([])
        self.assertEqual(result, [])

    def test_invalid_type_raises_error(self):
        """Does not work with parameters that are not a list."""
        invalid_inputs = [42, "hello", 3.14, None]
        for invalid_input in invalid_inputs:
            with self.subTest(invalid_input=invalid_input):
                with self.assertRaises(TypeError):
                    bubble_sort(invalid_input)


if __name__ == "__main__":
    unittest.main()
