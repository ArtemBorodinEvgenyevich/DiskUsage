import os
import sys
import unittest
from disk_usage import main, write_to_file


class TestMain(unittest.TestCase):

    def test_main(self):
        sys.argv = ['-e', '.p']
        self.assertRaises(FileNotFoundError, main)

    def test_write_to_file(self):
        raised = False
        path = os.path.dirname(__file__)

        try:
            write_to_file(path=path, tablefmt="simple",
                          tables=[], headers=[], colalign=[])
        except:
            raised = True

        self.assertFalse(raised, "Exception raised")



if __name__ == '__main__':
    unittest.main()
