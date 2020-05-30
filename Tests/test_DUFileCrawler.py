import os
import types
import unittest
from DiscUsage_Console.DUCore.DUFileCrawler import *


class TestFileCrawler(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.file_crawler = FileCrawler(path=os.path.dirname(__file__), abs_path=False)

    def test_get_files(self):
        generator = self.file_crawler.get_files()
        self.assertIsInstance(generator, types.GeneratorType)

        for file in generator:
            self.assertIsInstance(file, File)

            self.assertIsInstance(file.path, str)
            self.assertIsInstance(file.size, int)
            self.assertIn('.', file.extension)
            self.assertIsInstance(file.adate, str)
            self.assertIsInstance(file.mdate, str)
            self.assertIsInstance(file.size, int)
            self.assertIsInstance(file.inode, int)
            self.assertIsInstance(file.device, int)
            self.assertIsInstance(file.permissions, str)
            self.assertIsInstance(file.depth, int)


class TestFileCrawlerStaticMethods(unittest.TestCase):

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
        permission_expected = "-rwx-----"
        permission_actual = FileCrawler.get_file_permission(self.valid_root)
        self.assertEqual(permission_expected, f"{permission_actual[:4]}-----")


class TestFileTree(unittest.TestCase):

    def test_root_validation(self) -> None:
        # Test if throw exception
        self.assertRaises(FileNotFoundError, FileTree.root_validation, "/home/artem/Kek")

        # Test if gets a str type variable
        self.assertIsInstance(os.path.dirname(__file__), str)


if __name__ == '__main__':
    unittest.main()
