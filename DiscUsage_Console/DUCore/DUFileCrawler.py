# -*- coding: utf-8 -*-

from DUUtilities.DUFormatTools import FormatASCIIStyle, format_split_filename
from collections import namedtuple

import os
import sys
import argparse

File = namedtuple("File", ["path", "size", "extension"])


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
                # file = File()

                if self._args.absolute:
                    file_path = os.path.join(root, filename)
                else:
                    file_path = os.path.join(root, filename).rsplit(self._root)[1]
                file_size = os.stat(os.path.join(root, filename)).st_size
                file_extension = format_split_filename(filename)[1]

                file = File(path=file_path,
                            size=file_size,
                            extension=file_extension)

                yield file

    @staticmethod
    def root_validation(root: str):
        def check_path(path):
            if not os.path.exists(path):
                raise FileNotFoundError

        if root is not None:
            try:
                check_path(root)
            except FileNotFoundError as file_error:
                print("--------------------------------- ")
                print(f"{FormatASCIIStyle.RED}Error! ")
                print("Specified folder does not exist!")
                print(f"{file_error}")
                print(f"Try once again.{FormatASCIIStyle.RESET}")
                print("---------------------------------")
                sys.exit(2)

            return root

        else:

            return os.path.abspath(os.path.curdir)
