import unittest
import os
from DiscUsage_Console.DUCore.DUFileCrawler import FileCrawler


class TestFileCrawler(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.valid_root = FileCrawler.root_validation(os.path.dirname(__file__))

    def test_root_validation(self) -> None:
        # Test if throw exception
        self.assertRaises(FileNotFoundError, FileCrawler.root_validation, "/home/artem/Kek")

        # Test if gets a str type variable
        self.assertIsInstance(self.valid_root, str)

    def test_get_file_permission(self) -> None:
        # Test if current file permission is getting right
        # Defailt shoulld be -rw-rw-r--
        permission_expected = "-rwxrwxr-x"
        permission_actual = FileCrawler.get_file_permission(self.valid_root)
        self.assertEqual(permission_expected, permission_actual)

if __name__ == '__main__':
    unittest.main()
