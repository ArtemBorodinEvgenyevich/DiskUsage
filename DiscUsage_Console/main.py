# -*- coding: utf-8 -*-

from tabulate import tabulate
from DiscUsage_Console.DUCore.DUSpinner import Spinner
from DiscUsage_Console.DUCore.DUFileCrawler import FileCrawler
from DiscUsage_Console.DUCore.DUArgParser import ArgParser, ArgParserTablesInit
from DiscUsage_Console.DUUtilities.DUFormatTools import *

import sys


def main() -> None:
    # Init argument parser, threads and tables
    parser = ArgParser()
    args = parser.parse_args()
    tables_init = ArgParserTablesInit(args=args)
    crawler = FileCrawler(args=args)
    waiting_ico = Spinner()

    # Catching possible errors during program execution.
    try:
        waiting_ico.start()
        files = [file for file in crawler.get_files()]
        waiting_ico.stop()

        for file in files:
            tables_init.add_table(file)

        # Check for internal tabulate function error.
        # IndexError raised in case no elements in tables or invalid data passed.
        try:
            print(tables_init.headers, tables_init.colalign)
            output_tables = tabulate(tables_init.tables, headers=tables_init.headers,
                                     tablefmt="fancy_grid", colalign=tables_init.colalign)
            print(output_tables)
        except (IndexError, AttributeError) as error:
            format_print_error(exception=error, text="Tabulate error")
            sys.exit(4)

    except (FileNotFoundError, FileExistsError) as warning:
        waiting_ico.stop()
        format_print_warning(exception=warning, text="Crawling has been stopped.")
        sys.exit(2)
    except KeyboardInterrupt as warning:
        waiting_ico.stop()
        format_print_warning(exception=warning, text="Crawling has been stopped.")
        sys.exit(130)


if __name__ == '__main__':
    main()
