# -*- coding: utf-8 -*-

from os import path, walk, stat
from threading import Thread
from utilities.FormatTools import split_filename
from DataStruct import File


class FileCrawler:

    def __init__(self, root):
        super().__init__()

        self._root = root

    def run(self) -> None:
        self.get_files()

    def get_files(self):
        for root, dirs, files in walk(self._root):
            for filename in files:
                file = File()
                file.path = path.join(root, filename)
                file.size = stat(file.path).st_size
                file.extension = split_filename(filename)[1]

                yield file







