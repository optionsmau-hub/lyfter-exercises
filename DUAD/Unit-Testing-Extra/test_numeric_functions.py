import unittest
from numeric_functions import sum_numbers, average, celsius_to_fahrenheit
 
 
class TestSumNumbers(unittest.TestCase):
 
    def test_positive_numbers(self):
        self.assertEqual(sum_numbers([1, 2, 3]), 6)
 
    def test_negative_numbers(self):
        self.assertEqual(sum_numbers([-1, -2, -3]), -6)
 
    def test_zeros(self):
        self.assertEqual(sum_numbers([0, 0, 0]), 0)
 
 
class TestAverage(unittest.TestCase):
 
    def test_positive_numbers(self):
        self.assertEqual(average([2, 4, 6]), 4.0)
 
    def test_negative_numbers(self):
        self.assertEqual(average([-2, -4, -6]), -4.0)
 
    def test_zeros(self):
        self.assertEqual(average([0, 0, 0]), 0.0)
 
 
class TestCelsiusToFahrenheit(unittest.TestCase):
 
    def test_positive_temperature(self):
        self.assertEqual(celsius_to_fahrenheit(100), 212.0)
 
    def test_negative_temperature(self):
        self.assertEqual(celsius_to_fahrenheit(-40), -40.0)
 
    def test_zero_temperature(self):
        self.assertEqual(celsius_to_fahrenheit(0), 32.0)
 
 
if __name__ == "__main__":
    unittest.main()
 
