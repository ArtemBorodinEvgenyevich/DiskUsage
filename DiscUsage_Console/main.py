# -*- coding: utf-8 -*-
from tabulate import tabulate
from DiscUsage_Console.DUCore.DUSpinner import Spinner
from DiscUsage_Console.DUCore.DUFileCrawler import FileCrawler
from DiscUsage_Console.DUUtilities.DUFormatTools import format_convert_size, FormatASCIIStyle
import sys
import os


def check_path(search_path: str):
    """
    Utility for checking paths' existence.

    :param search_path:
    :return:
    """
    if not os.path.exists(search_path):
        raise FileNotFoundError

    return search_path


def main() -> None:
    """
    Main cycle. Yeaah!!!

    .. note::

        Another junk info about module. Please rewrite me
    """

    path = os.path.abspath(os.path.curdir)
    args = sys.argv

    if len(args) > 1:
        try:
            path = check_path(args[1])
        except FileNotFoundError:
            print("--------------------------------- ")
            print(f"{FormatASCIIStyle.RED}Error! ")
            print("Specified folder does not exist!")
            print(f"Try once again.{FormatASCIIStyle.RESET}")
            print("---------------------------------")
            sys.exit(2)

    tables = []

    crawler = FileCrawler(root=path)
    waiting_ico = Spinner()

    # Catching possible errors during program execution
    try:
        waiting_ico.start()
        files = [file for file in crawler.get_files()]
        waiting_ico.stop()

        for file in files:
            table = [file.path, format_convert_size(file.size), file.extension]
            tables.append(table)

        # Check for internal tabulate function errors.
        # IndexError raised in case using inappropriate data.
        try:
            headers = ["PATH", "SIZE", "EXTENSION"]
            output_tables = tabulate(tables, headers=headers, tablefmt="fancy_grid",
                                     colalign=("left", "center", "center"))
            print(output_tables)
        except IndexError as table_error:
            print("\r--------------------------------- ")
            print("Whoops! Something went wrong...")
            print(f"{FormatASCIIStyle.RED}{table_error}{FormatASCIIStyle.RESET}")
            print("---------------------------------")
            sys.exit(4)

    except KeyboardInterrupt:
        waiting_ico.stop()
        print("\r--------------------------------- ")
        print("Crawling has been stopped.")
        print(f"{FormatASCIIStyle.YELLOW}Keyboard interruption.{FormatASCIIStyle.RESET}")
        print("---------------------------------")
        sys.exit(130)


if __name__ == '__main__':
    main()
