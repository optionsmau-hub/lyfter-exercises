import unittest
from unittest.mock import patch, mock_open
from read_lines import read_lines
 
 
class TestReadLines(unittest.TestCase):
 
    def test_returns_expected_lines_without_creating_real_file(self):
        """Uses unittest.mock to simulate file content and verifies the
        expected lines are returned without creating a real file."""
        fake_file_content = "line 1\nline 2\nline 3\n"
        with patch("builtins.open", mock_open(read_data=fake_file_content)):
            result = read_lines("fake_path.txt")
        self.assertEqual(result, ["line 1\n", "line 2\n", "line 3\n"])
 
    def test_raises_file_not_found_error_when_file_does_not_exist(self):
        """Checks that read_lines raises FileNotFoundError if the file
        does not exist."""
        with patch("builtins.open", side_effect=FileNotFoundError):
            with self.assertRaises(FileNotFoundError):
                read_lines("nonexistent_file.txt")
 
 
if __name__ == "__main__":
    unittest.main()
 
