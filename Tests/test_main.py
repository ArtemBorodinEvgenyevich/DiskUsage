import sys
import unittest
from disk_usage import main


class TestMain(unittest.TestCase):

    def test_main(self):
        sys.argv = ['-e', '.p']
        self.assertRaises(FileNotFoundError, main)


if __name__ == '__main__':
    unittest.main()
