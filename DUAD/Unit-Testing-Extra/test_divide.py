import unittest
from divide import divide
 
 
class TestDivide(unittest.TestCase):
 
    def test_successful_division(self):
        """Validates that divide(10, 2) returns 5.0."""
        self.assertEqual(divide(10, 2), 5.0)
 
    def test_division_by_zero_raises_value_error(self):
        """Verifies that dividing by zero raises a ValueError."""
        with self.assertRaises(ValueError):
            divide(10, 0)
 
    def test_invalid_type_raises_type_error(self):
        """Validates that dividing with a string raises a TypeError."""
        with self.assertRaises(TypeError):
            divide(10, "a")
 
 
if __name__ == "__main__":
    unittest.main()
 
