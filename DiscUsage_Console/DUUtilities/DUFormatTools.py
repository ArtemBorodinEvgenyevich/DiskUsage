# -*- coding: utf-8 -*-
import math
from os import path
import argparse


class FormatASCIIStyle:
    """Structure provided special ASCII characters for console output editing."""
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
        Create own unique ASCII symbol style.

        :param mode:
        :param colour:
        :param background:
        :return:
        """
        return f"\033[{mode};{colour};{background}m"


def format_convert_size(size_bytes: int):
    """
    Utility for human-read size conversion.

    :param size_bytes:
    :return:
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
    Utility for splitting filename from extension.

    :param filename:
    :return:
    """
    if len(filename.split(".")) > 2:
        return filename.split('.')[0], '.'.join(filename.split('.')[-2:])
    return path.splitext(filename)


def format_columns(args: argparse.Namespace):
    headers = ["PATH", "SIZE", "EXTENSION"]
    colalign = ["left", "center", "center"]

    if args.owner:
        headers.append("USER")
        headers.append("GROUP")
        colalign.append("center")
        colalign.append("center")
    if args.inode:
        headers.append("INODE")
        colalign.append("center")
    if args.device:
        headers.append("DEVICE")
        colalign.append("center")
    if args.links:
        headers.append("LINKS")
        colalign.append("center")

    if args.adate:
        headers.append("ACCESS")
        colalign.append("center")
    if args.mdate:
        headers.append("MODIFIED")
        colalign.append("center")

    return headers, colalign


# FIXME: see if docs displays correctly. Repair if not.
def format_print_error(exception: BaseException, text: str = "Error"):
    print("\r--------------------------------- ")
    print(text)
    print(f"{FormatASCIIStyle.RED}{exception}{FormatASCIIStyle.RESET}")
    print("Please, try again.")
    print("\r--------------------------------- ")


def format_print_warning(exception: BaseException, text: str = "Error"):
    print("\r--------------------------------- ")
    print(text)
    print(f"{FormatASCIIStyle.YELLOW}{exception}{FormatASCIIStyle.RESET}")
    print("\r--------------------------------- ")
