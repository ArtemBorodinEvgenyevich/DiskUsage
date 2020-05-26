# -*- coding: utf-8 -*-
"""A module containing functions for text formatting"""
import os
import math


class FormatASCIIStyle:
    """Structure provided ANSI escape sequences for console output editing."""
    RESET = "\033[0m"
    CLEAR = "\033[2J"

    GREY = "\033[0;30;40m"
    RED = "\033[0;31;40m"
    GREEN = "\033[0;32;40m"
    YELLOW = "\033[0;33;40m"
    BLUE = "\033[0;34;40m"
    PURPLE = "\033[0;35;40m"
    CYAN = "\033[0;36;40m"
    WHITE = "\033[0;37;40m"

    NORMAL = "\033[0;37;40m"
    BRIGHT = "\033[1;37;40m"
    ITALIC = "\033[3;37;40m"
    UNDERLINE = "\033[4;37;40m"
    BLINK = "\033[5;37;40m"

    @staticmethod
    def custom_style(mode: int, colour: int, background: int):
        """
        Create custom style for ASCII characters output.
        You can combine: char style(mode), char colour and char background color
        to create unique output.

        .. note::
            Use ``RESET`` sequence after using your style to return to default char style.

        * mode: ``NORMAL``, ``BRIGHT``, ``ITALIC``, ``UNDERLINE``, ``BLINK``
        * colour: ``GREY``, ``RED``, ``GREEN``, ``YELLOW``, ``BLUE``, ``PURPLE``, ``CYAN``, ``WHITE``
        * special: ``RESET``, ``CLEAR``

        :param mode: **--** char style sequence
        :param colour: **--** char colour sequence
        :param background: **--** char background colour sequence
        :return: **--** escape sequence
        :rtype: **--** ``string``
        """
        return f"\033[{mode};{colour};{background}m"


def format_convert_size(size_bytes: int):
    """
    Convert bytes to human-read metrics.

    :param size_bytes: **--** bytes to convert
    :return: **--** string with size and size name
    :rtype: **--** ``string``
    """
    if size_bytes == 0:
        return "0B"

    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")

    dimension = int(math.floor(math.log(size_bytes, 1024)))
    power = math.pow(1024, dimension)
    size = round(size_bytes / power, 2)

    return str(f"{size} {size_name[dimension]}")


def format_split_filename(filename: str):
    """
    Split file name from its extension like ``.png`` or ``.tar.gz``

    :param filename: **--** file name to separate from extension
    :return: **--** extension name
    :rtype: **--** ``string``
    """
    if len(filename.split(".")) > 2:
        return filename.split('.')[0], '.'.join(filename.split('.')[-2:])
    return os.path.splitext(filename)


def format_extract_depth(searchpath: str, fullpath: str):
    """Get number of file depth relative to search root.

    :param searchpath: **--** file search root
    :param fullpath: **--** full path to file
    :return: **--** difference between amount of separators in param paths
    :rtype: **--** ``int``
    """
    searchpath_sep = searchpath.count(os.sep)
    fullpath_sep = fullpath.count(os.sep)
    return fullpath_sep - searchpath_sep


def format_replace_char(string: str, char: str, index: int):
    """Replace specific char in string.

    :param string: **--** string to modify
    :param char: **--** changed char
    :param index: **--** char index in string to replace
    :return: **--** modified string
    :rtype: **--** ``str``
    """
    return string[:index] + char + string[index + 1:]


# FIXME: see if docs displays correctly. Repair if not.
def format_print_error(exception: BaseException, text: str = "Error") -> None:
    """Print a well formatted error message. Output error will be coloured in red.

    :param exception: **--** caught exception to output
    :param text: **--** message text output
    """
    print("\r--------------------------------- ")
    print(text)
    print(f"{FormatASCIIStyle.RED}{exception}{FormatASCIIStyle.RESET}")
    print("Please, try again.")
    print("\r--------------------------------- ")


def format_print_warning(exception: BaseException, text: str = "Error") -> None:
    """Print a well formatted warning message. Output warning will be coloured in yellow.

    :param exception: **--** caught exception to output
    :param text: **--** message text output
    """
    print("\r--------------------------------- ")
    print(text)
    print(f"{FormatASCIIStyle.YELLOW}{exception}{FormatASCIIStyle.RESET}")
    print("\r--------------------------------- ")
