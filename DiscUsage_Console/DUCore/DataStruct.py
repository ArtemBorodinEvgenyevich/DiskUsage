# -*- coding: utf-8 -*-


class File:
    """File structure."""
    def __init__(self):
        super().__init__()

        self._path = ""
        self._ext = ""
        self._size = 0

    @property
    def path(self):
        """

        :return:
        """
        return self._path

    @path.setter
    def path(self, file_path: str):
        """

        :param file_path:
        :return:
        """
        self._path = file_path

    @property
    def size(self):
        """

        :return:
        """
        return self._size

    @size.setter
    def size(self, file_size: int):
        """

        :param file_size:
        :return:
        """
        self._size = file_size

    @property
    def extension(self):
        """

        :return:
        """
        return self._ext

    @extension.setter
    def extension(self, file_extension: str):
        """

        :param file_extension:
        :return:
        """
        self._ext = file_extension
