# -*- coding: utf-8 -*-

from tabulate import tabulate
from DUCore.DUSpinner import Spinner
from DUCore.DUFileCrawler import FileCrawler
from DUCore.DUArgParser import ArgParser
from DUUtilities.DUFormatTools import format_convert_size, FormatASCIIStyle

import sys
import os


def check_path(search_path: str):
    if not os.path.exists(search_path):
        raise FileNotFoundError

    return search_path


def main() -> None:
    # Init argument parser, threads and tables
    parser = ArgParser(description='DiskUsage [OPTIONS] <SEARCH_DIR> \n\t'
                                   'Lists files contained in a specified directory.\n\t'
                                   'Generates an ASCII table with file path and its size.\n')
    args = parser.parse_args()
    tables = []
    crawler = FileCrawler(args=args)
    waiting_ico = Spinner()

    # Catching possible errors during program execution.
    try:
        waiting_ico.start()
        files = [file for file in crawler.get_files()]
        waiting_ico.stop()

        for file in files:
            # Check for pattern match if arguments enabled.
            if args.extension is not None and file.extension != args.extension:
                continue
            table = [file.path, format_convert_size(file.size), file.extension]
            tables.append(table)

        # Check for internal tabulate function error.
        # IndexError raised in case no elements in tables or invalid data passed.
        try:
            headers = ["PATH", "SIZE", "EXTENSION"]
            output_tables = tabulate(tables, headers=headers, tablefmt="fancy_grid",
                                     colalign=("left", "center", "center"))
            print(output_tables)
        except (IndexError, AttributeError) as table_error:
            print("\r--------------------------------- ")
            print("There are no such files.")
            print("Please, try again.")
            print(f"{FormatASCIIStyle.RED}{table_error}{FormatASCIIStyle.RESET}")
            print("---------------------------------")
            sys.exit(4)

    except (KeyboardInterrupt, FileNotFoundError, FileExistsError) as runtime_error:
        waiting_ico.stop()
        print("\r--------------------------------- ")
        print("Crawling has been stopped.")
        print(f"{FormatASCIIStyle.YELLOW}{runtime_error}{FormatASCIIStyle.RESET}")
        print("---------------------------------")
        sys.exit(130)


if __name__ == '__main__':
    main()
