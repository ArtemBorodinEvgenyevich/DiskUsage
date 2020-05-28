import os
import time
import unittest
from DiscUsage_Console.DUCore.DUArgParser import *
from DiscUsage_Console.DUCore.DUFileCrawler import FileCrawler, File


class TestArgParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.parser = ArgParser()

    def test_parser(self):
        sys_args = ['-a', '-l', '-p', '-t', '-w',
                    '-A', '-M', '-i', '-d', '-sdt']
        args = self.parser.parse_args(sys_args)

        self.assertTrue(args.absolute)
        self.assertTrue(args.links)
        self.assertTrue(args.permissions)
        self.assertTrue(args.tree)
        self.assertTrue(args.owner)
        self.assertTrue(args.adate)
        self.assertTrue(args.mdate)
        self.assertTrue(args.inode)
        self.assertTrue(args.device)
        self.assertTrue(args.sort_depth_top)


class TestParserTablesInit(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        args = ArgParser().parse_args(['-l', '-p', '-t', '-w', '-A',
                                       '-M', '-i', '-d', '-sdt'])
        crawler = FileCrawler(os.path.dirname(__file__), abs_path=False)
        stats = os.stat(os.path.abspath(__file__))

        cls.permission = crawler.get_file_permission(os.path.abspath(__file__))
        cls.adate = time.ctime(stats.st_atime)
        cls.user = stats.st_uid
        cls.group = stats.st_gid
        cls.tables_init = ArgParserTablesInit(args=args)
        cls.files = [file for file in crawler.get_files()]

    def test_add_table(self):
        dict_pos = 0
        expected_list = sorted(["PATH", "SIZE", "EXTENSION", "LINKS", "PERMISSIONS",
                                "ACCESS", "MODIFIED", "INODE", "DEVICE", "USER", "GROUP"])

        for file in self.files:
            self.tables_init.add_table(file)
            actual_list = sorted(list(self.tables_init._tables[dict_pos].keys()))
            dict_pos += 1

            self.assertListEqual(expected_list, actual_list[:-1])

    def test_headers(self):
        expected_list = sorted(["PATH", "SIZE", "EXTENSION", "LINKS", "PERMISSIONS",
                                "ACCESS", "MODIFIED", "INODE", "DEVICE", "USER", "GROUP"])
        for file in self.files:
            self.tables_init.add_table(file)
        actual_list = sorted(self.tables_init.headers[:-1])

        self.assertListEqual(expected_list, actual_list)

    def test_colalign(self):
        expected_list = ("left", 'center', 'center', 'center', 'center', 'center',
                         'center', 'center', 'center', 'center', 'center', 'center')
        for file in self.files:
            self.tables_init.add_table(file)
        actual_list = self.tables_init.colalign

        self.assertTupleEqual(expected_list, actual_list)

    def test_tables(self):

        expected_list = ["home/artem", "9.77 KB", ".py",  pwd.getpwuid(self.user).pw_name,
                         pwd.getpwuid(self.group).pw_name, 40, 40, 1, self.permission,
                         self.adate, self.adate]

        test_file = File(path="home/artem", size=10000, extension=".py", links=1,
                         permissions=self.permission, group_owner=self.user, user_owner=self.group,
                         adate=self.adate, mdate=self.adate, inode=40, device=40, depth=4)

        self.tables_init.add_table(test_file)
        actual_list = self.tables_init.tables[0]

        print(expected_list)
        print(actual_list)

        self.assertListEqual(expected_list, actual_list)


if __name__ == '__main__':
    unittest.main()
