# -*- coding: utf-8 -*-
"""A module containing class for extracting files and theirs attributes from specified path.
"""
from DUUtilities.DUFormatTools import *
from ctypes import c_ulong
from collections import namedtuple

import os
import sys
import stat
import time
import argparse

if sys.platform == "win32":
    from DUUtilities.DUWinSecurityInfo import get_file_security


File = namedtuple("File", ["path", "size", "extension",
                           "adate", "mdate", "links",
                           "user_owner", "group_owner",
                           "inode", "device", "permissions",
                           "depth"])
"""File attributes:

.. py:attribute:: path
        
    **-** path to the found file
    
     .. note::
        Depending on command-line arguments can be absolute or relative.
        
    
.. py:attribute:: size

    **-** file size in bytes
    
.. py:attribute:: extension

    **-** file extension

.. py:attribute:: adate

    **-** the most recent file access date
    
.. py:attribute:: mdate

    **-** the most recent file content modification date
    
.. py:attribute:: links

    **-** overall amount of links to the file

.. py:attribute:: user_owner

    **-** file owner user ID
    
    .. note::
        Owner ID converted to name.

.. py:attribute:: group_owner

    **-** file group owner ID
    
    .. note::
        Will not be used on **Windows OS**. Default value: ``None``

.. py:attribute:: inode

    **-** inode structure ID
    
    .. note::
        File ID will be shown instead of inode if using **Windows OS**.

.. py:attribute:: device

    **-** device ID the file inode/file id resides on
    
.. py:attribute:: permissions

    **-** file read, write and execute permissions for different groups
    
.. py:attribute:: depth
    
    **-** file depth in a file tree
    
    .. warning::
        Due to different hacks for file sorting, this parameter should be always placed in the end.
"""


class FileCrawler:
    """Class for file searching and file attributes extraction."""

    def __init__(self, args: argparse.Namespace):
        """

        :param args: **-** command line arguments for processing
        :type args: **-** :class:``argparse.Namespace``
        """
        super().__init__()

        self._args = args
        self._root = self.root_validation(args.search_dir)

    def get_files(self):
        """Start recursive search in specified path for files and theirs attributes.

        .. note::
            Extracts all listed file attributes, no matter were they specified by command-line arguments.

        :return: **--** generator with files
        :rtype: **-** ``iter``
        """
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
                # Using ctypes to avoid negative value on Linux
                file_inode = c_ulong(stats.st_ino).value
                file_device = stats.st_dev
                file_permissions = self.get_file_permission(os.path.join(root, filename))
                file_depth = format_extract_depth(self._root, os.path.join(root, filename))

                if sys.platform == "win32":
                    pSD = get_file_security(os.path.join(root, filename))
                    file_user_owner, file_owner_domain, owner_sid_type = pSD.get_owner()
                    if file_owner_domain:
                        file_user_owner = f"{file_owner_domain}\\{file_user_owner} ({owner_sid_type})"
                        file_group_owner = None
                else:
                    file_user_owner = stats.st_uid
                    file_group_owner = stats.st_gid

                file = File(path=file_path, size=file_size, extension=file_extension,
                            adate=file_a_time, mdate=file_m_time, links=file_links_num,
                            user_owner=file_user_owner, group_owner=file_group_owner,
                            inode=file_inode, device=file_device, permissions=file_permissions,
                            depth=file_depth)

                yield file

    @staticmethod
    def root_validation(root: str):
        """Check if specified path do exist.

        .. note::
            If path was not specified, then current dir path is taken.

        :param root: **--** specified path to validate
        :exception exception: **-** ``FileNotFound``
        :return: **--** path to search in
        :rtype: **-** ``string``
        """
        def check_path(path):
            if not os.path.exists(path):
                raise FileNotFoundError

        if root is not None:
            check_path(root)
            return root
        else:
            return os.path.abspath(os.path.curdir)


    @staticmethod
    def get_file_permission(path: str):
        """Get file permission mask bits and interpret them in Unix-like form.

        :param path: **--** path to file
        :return: **--** string which represents Unix-like file permissions: :mod:`-rwxrwxrwx`
        :rtype: **-** ``string``
        """
        output = "---------"
        mask = os.stat(path).st_mode
        if bool(mask & stat.S_IRUSR):
            output = format_replace_char(output, 'r', 1)
        if bool(mask & stat.S_IWUSR):
            output = format_replace_char(output, 'w', 2)
        if bool(mask & stat.S_IXUSR):
            output = format_replace_char(output, 'x', 3)
        if bool(mask & stat.S_IRGRP):
            output = format_replace_char(output, 'r', 4)
        if bool(mask & stat.S_IWGRP):
            output = format_replace_char(output, 'w', 5)
        if bool(mask & stat.S_IXGRP):
            output = format_replace_char(output, 'x', 6)
        if bool(mask & stat.S_IROTH):
            output = format_replace_char(output, 'r', 7)
        if bool(mask & stat.S_IWOTH):
            output = format_replace_char(output, 'w', 8)
        if bool(mask & stat.S_IXOTH):
            output = format_replace_char(output, 'x', 9)

        return output
