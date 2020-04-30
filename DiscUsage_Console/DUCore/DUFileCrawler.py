# -*- coding: utf-8 -*-

from os import path, walk, stat
from threading import Thread
from DiscUsage_Console.DUUtilities.DUFormatTools import format_split_filename
from DiscUsage_Console.DUCore.DUDataStruct import File


class FileCrawler:
    """File searching."""
    def __init__(self, root):
        """

        :param root:
        """
        super().__init__()

        self._root = root

    def run(self) -> None:
        self.get_files()

    def get_files(self):
        """

        :return:
        """
        for root, dirs, files in walk(self._root):
            for filename in files:
                file = File()
                file.path = path.join(root, filename)
                file.size = stat(file.path).st_size
                file.extension = format_split_filename(filename)[1]

                yield file







