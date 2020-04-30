# -*- coding: utf-8 -*-
from tabulate import tabulate
from DiscUsage_Console.DUCore.Spinner import Spinner
from DiscUsage_Console.DUCore.FileCrawler import FileCrawler
from DiscUsage_Console.utilities.FormatTools import convert_size, ASCIIStyle
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


def main():
    """
    Main cycle. Yeaah!!!

    :return:
    """
    path = os.path.abspath(os.path.curdir)
    args = sys.argv

    if len(args) > 1:
        try:
            path = check_path(args[1])
        except FileNotFoundError:
            print("--------------------------------- ")
            print(f"{ASCIIStyle.RED}Error! ")
            print("Specified folder does not exist!")
            print(f"Try once again.{ASCIIStyle.RESET}")
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
            table = [file.path, convert_size(file.size), file.extension]
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
            print(f"{ASCIIStyle.RED}{table_error}{ASCIIStyle.RESET}")
            print("---------------------------------")
            sys.exit(4)

    except KeyboardInterrupt:
        waiting_ico.stop()
        print("\r--------------------------------- ")
        print("Crawling has been stopped.")
        print(f"{ASCIIStyle.YELLOW}Keyboard interruption.{ASCIIStyle.RESET}")
        print("---------------------------------")
        sys.exit(130)


if __name__ == '__main__':
    main()
