import os


class File:
    def __init__(self):
        super().__init__()

        self._path = ""
        self._ext = ""
        self._size = 0

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, file_path: str):
        self._path = file_path

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, file_size: int):
        self._size = file_size

    @property
    def extension(self):
        return self._ext

    @extension.setter
    def extension(self, file_extension: str):
        self._ext = file_extension
