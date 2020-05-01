# -*- coding: utf-8 -*-

from DiscUsage_Console.DUUtilities.DUFormatTools import format_split_filename, format_print_error
from collections import namedtuple

import os
import time
import argparse
from ctypes import c_ulong


File = namedtuple("File", ["path", "size", "extension",
                           "adate", "mdate", "links",
                           "user_owner", "group_owner",
                           "inode", "device"])


class FileCrawler:
    """File searching."""

    def __init__(self, args: argparse.Namespace):
        super().__init__()

        self._args = args
        self._root = self.root_validation(args.search_dir)

    def run(self) -> None:
        self.get_files()

    def get_files(self):
        for root, dirs, files in os.walk(self._root):
            for filename in files:

                stats = os.stat(os.path.join(root, filename))

                if self._args.absolute:
                    file_path = os.path.join(root, filename)
                else:
                    file_path = os.path.join(root, filename).rsplit(self._root)[1]
                file_size = stats.st_size
                file_extension = format_split_filename(filename)[1]
                file_a_time = time.ctime(stats.st_atime)
                file_m_time = time.ctime(stats.st_mtime)
                file_links_num = stats.st_nlink
                file_user_owner = stats.st_uid
                file_group_owner = stats.st_gid
                # Using ctypes to avoid negative value on Linux
                file_inode = c_ulong(stats.st_ino).value
                file_device = stats.st_dev

                file = File(path=file_path, size=file_size, extension=file_extension,
                            adate=file_a_time, mdate=file_m_time, links=file_links_num,
                            user_owner=file_user_owner, group_owner=file_group_owner,
                            inode=file_inode, device=file_device)

                yield file

    @staticmethod
    def root_validation(root: str):
        def check_path(path):
            if not os.path.exists(path):
                raise FileNotFoundError

        if root is not None:
            check_path(root)
            return root
        else:
            return os.path.abspath(os.path.curdir)
