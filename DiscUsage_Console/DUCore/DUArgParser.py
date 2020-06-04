# -*- coding: utf-8 -*-
"""A module containing classes that deal with python built-in ``argparse`` module.

.. note::
    
    May not properly work on Windows due to lack of pwd module.
    Reinstall python interpreter if no ``winpwd`` was found.

"""

import sys
import argparse
from DiscUsage_Console.DUUtilities.DUFormatTools import format_convert_size

try:
    import pwd
except ImportError:
    pass


class ArgParser(argparse.ArgumentParser):
    """Base class to define and parse command-line options and arguments."""

    def __init__(self):
        super().__init__()

        self.description = 'DiskUsage [OPTIONS] <SEARCH_DIR>.\n\t' \
                           'Lists files contained in a specified directory.\n\t' \
                           'Generates an ASCII table with file path and its size.\n' \
                           'For more info run `host_docs_local.py` from docs folder\n'

        self.add_argument("search_dir", nargs='?', help="Files searching directory. If not specified current "
                                                        "directory is used.")

        self.add_argument("-a", "--absolute", action="store_true", help="show absolute path to file")
        self.add_argument("-e", "--extension", type=str, help="show files match specified extension")
        self.add_argument("-l", "--links", action="store_true", help="show number of links to the inode")
        self.add_argument("-o", "--output", nargs=2, metavar=("FILEPATH", "STYLE"), help="write result to file")
        self.add_argument("-p", "--permissions", action="store_true", help="show file permissions in Unix-like form")
        self.add_argument("-t", "--tree", action="store_true", help="show dir content instead of statistics")
        self.add_argument("-w", "--owner", action="store_true", help="show file owner")

        self.add_argument("-A", "--adate", action="store_true", help="show date of most recent access")
        self.add_argument("-M", "--mdate", action="store_true", help="show date of most recent content "
                                                                     "modification")

        self.add_argument("-i", "--inode", action="store_true", help="show inode number")
        self.add_argument("-d", "--device", action="store_true", help="show device inode resides on")

        self.add_argument("-spu", "--sort_permission_user", type=str, help="sort by user permission by adding string "
                                                                           "after: {-p rw :r - by read, w - by write}")
        self.add_argument("-spg", "--sort_permission_group", type=str, help="sort by group permission by adding string "
                                                                            "after: {-p rw :r - by read, w - by write}")
        self.sort_group = self.add_mutually_exclusive_group()
        self.sort_group.add_argument("-sdt", "--sort_depth_top", action="store_true",
                                     help="sort output result by file depth from top to bottom")
        self.sort_group.add_argument("-sdb", "--sort_depth_bottom", action="store_true",
                                     help="sort output result by file depth from bottom to top")
        self.sort_group.add_argument("-ssh", "--sort_size_high", action="store_true",
                                     help="sort output by file size from high to low")
        self.sort_group.add_argument("-ssl", "--sort_size_low", action="store_true",
                                     help="sort output by file size from low to high")


class ArgParserTablesInit:
    """Class for tables, headers and column alignment initialization.

    .. warning::

        Do not recall :py:func:`tables` property in case you have already use it!
        It will try to operate with non-existing dictionary which leads to :class:`IndexError` exception.

    """

    def __init__(self, args: argparse.Namespace):

        self.args = args

        self._headers = []
        self._colalign = ["left"]
        self._tables = []

    # FIXME: put proper instance name in file param
    def add_table(self, file: 'File'):
        """

        :param file: **--** reference to the :class:`DUCore.DUFileCrawler.File` named tuple.
        :return: **-** list of files' attributes represented as dictionary.
        :rtype: **-** ``list``
        """
        if self.args.extension is not None and file.extension != self.args.extension:
            return

        if self.args.sort_permission_user is not None:
            permission = f"{file.permissions[1]}{file.permissions[2]}"
            if self.args.sort_permission_user not in permission:
                return

        if self.args.sort_permission_group is not None:
            permission = f"{file.permissions[4]}{file.permissions[5]}"
            if self.args.sort_permission_group not in permission:
                return

        table = {"PATH": file.path, "SIZE": format_convert_size(file.size), "EXTENSION": file.extension}

        if self.args.owner:
            # TODO: move to DUFileCrawler
            # Interpret id as user/group name
            table.update({"USER": pwd.getpwuid(file.user_owner).pw_name})
            table.update({"GROUP": pwd.getpwuid(file.group_owner).pw_name})

        if self.args.inode:
            table.update({"INODE": file.inode})

        if self.args.device:
            table.update({"DEVICE": file.device})

        if self.args.links:
            table.update({"LINKS": file.links})

        if self.args.permissions:
            table.update({"PERMISSIONS": file.permissions})

        if self.args.adate:
            table.update({"ACCESS": file.adate})

        if self.args.mdate:
            table.update({"MODIFIED": file.mdate})

        # Here's a dirty trick for depth/size sort.
        # Added elements will be removed after tables sort.
        # These args check ALWAYS should be the last!
        if self.args.sort_depth_top or self.args.sort_depth_bottom:
            table.update({"depth": file.depth})
        elif self.args.sort_size_high or self.args.sort_size_low:
            table.update({"size": file.size})

        self._tables.append(table)

    @property
    def headers(self):
        """Access to generated headers.
        Original - :func:`self._headers` class attribute


        :return: **-** list of generated table headers
        :rtype: **-** ``list``
        """
        self._headers = list(self._tables[0].keys())

        return self._headers

    @property
    def colalign(self):
        """Access to generated column alignment arguments.
        Original - :func:`self._colalign` class attribute


        .. note::
            Converts ``list`` to ``tuple``. This is requested by :mod:`tabulate` module.

        :return: **-** list of column alignment flags
        :rtype: **-** ``tuple``
        """
        cnt = self.headers[1:]
        for _ in cnt:
            self._colalign.append("center")

        # Convert colalign to tuple requested by "tabulate"
        return tuple(self._colalign)

    # FIXME: clean up this mess!
    @property
    def tables(self):
        """Access to generated tables (`file attributes to show`).
        Original - :func:`self._tables` class attribute

        .. note::
            A little hack was implemented for file **depth** and size **sorting**.
            These file attributes have been transferred among other attributes but they should not be shown.
            Method deletes the last dictionaru pair.

        .. note::
            Fills :func:`self._headers` class field after execution.

        .. warning::
            It will remove

        :return: **-** list with print ready tables content
        :rtype: **-** ``list``
        """
        t = []
        if self.args.sort_depth_bottom:
            sorted_tables = sorted(self._tables, key=lambda x: (x.get("depth"), len(x.get("PATH"))))
            for i in sorted_tables:
                i.pop("depth")
                t.append(list(i.values()))
        elif self.args.sort_depth_top:
            sorted_tables = sorted(self._tables, key=lambda x: (x.get("depth"), len(x.get("PATH"))), reverse=True)
            for i in sorted_tables:
                i.pop("depth")
                t.append(list(i.values()))
        elif self.args.sort_size_low:
            sorted_tables = sorted(self._tables, key=lambda x: (x.get("size"), len(x.get("PATH"))))
            for i in sorted_tables:
                i.pop("size")
                t.append(list(i.values()))
        elif self.args.sort_size_high:
            sorted_tables = sorted(self._tables, key=lambda x: (x.get("size"), len(x.get("PATH"))), reverse=True)
            for i in sorted_tables:
                i.pop("size")
                t.append(list(i.values()))
        else:
            for i in self._tables:
                t.append(list(i.values()))

        return t
