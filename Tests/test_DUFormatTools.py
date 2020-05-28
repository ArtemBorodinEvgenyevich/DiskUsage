import unittest
from DiscUsage_Console.DUUtilities.DUFormatTools import *


class TestFormatTools(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.valid_path_file = os.path.abspath(__file__)
        cls.valid_path_dir = os.path.dirname(__file__)
        cls.format_ascii = FormatASCIIStyle()

    def test_replace_char(self):
        # Test char replacement in string

        string_expected = "-*-*-*-"
        string_actual = "-------"

        cnt = 1
        for i in range(3):
            string_actual = format_replace_char(string_actual, '*', i + cnt)
            cnt += 1

        self.assertEqual(string_actual, string_expected)

    def test_split_filename(self):
        # Test if filename separated from file extension correctly

        expected = ("/home/artem/Documents/testcase", "tar.gz")
        actual = "/home/artem/Documents/testcase.tar.gz"

        output = format_split_filename(actual)
        self.assertEqual(expected, output)

    def test_extract_depth(self):
        # Test if file depth from Test dir is getting correctly

        expected = 1
        actual = format_extract_depth(self.valid_path_dir, self.valid_path_file)
        self.assertEqual(expected, actual)

    def test_convert_size(self):
        # Test if size converted correctly

        expected = "9.77 KB"
        actual = format_convert_size(10000)
        self.assertEqual(expected, actual)

    def test_custom_style(self):
        expected = "\033[4;34;30m"
        actual = self.format_ascii.custom_style(4, 34, 30)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
