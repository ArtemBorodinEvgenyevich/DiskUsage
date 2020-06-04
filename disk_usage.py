# -*- coding: utf-8 -*-
"""Enter point for :mod:`DiskUsage_Console`

Creates tables for output and catches possible exceptions that might occur at a runtime.

"""

from tabulate import tabulate
from DiscUsage_Console.DUCore.DUSpinner import Spinner
from DiscUsage_Console.DUCore.DUFileCrawler import FileCrawler, FileTree
from DiscUsage_Console.DUCore.DUArgParser import *
from DiscUsage_Console.DUUtilities.DUFormatTools import *


def write_to_file(path, tablefmt, tables, headers, colalign):
    try:
        with open(path, 'w') as out_file:

            # Try to use user defined table style

            try:
                output_tables = tabulate(tables, headers=headers,
                                         tablefmt=tablefmt, colalign=colalign)
                out_file.write(output_tables)
            except IndentationError:

                output_tables = tabulate(tables, headers=headers,
                                         tablefmt="simple", colalign=colalign)
                out_file.write(output_tables)

    except (IsADirectoryError, FileNotFoundError) as error:
        format_print_warning(exception=error, text="File hasn't been written")


def main() -> None:
    """Main script to execute."""

    # Init argument parser, threads and tables
    parser = ArgParser()
    args = parser.parse_args()

    # Check if tree output only
    if args.tree:
        FileTree(path=args.search_dir).print_tree()
        sys.exit(0)

    tables_init = ArgParserTablesInit(args=args)
    crawler = FileCrawler(path=args.search_dir, abs_path=args.absolute)
    waiting_ico = Spinner()

    # Catching possible errors during program execution.
    # Getting file info
    try:
        waiting_ico.start()
        files = [file for file in crawler.get_files()]
        waiting_ico.stop()

        for file in files:
            tables_init.add_table(file)

        # Check for internal tabulate function error.
        # IndexError raised in case no elements in tables or invalid data passed.
        try:
            # Print result
            # Init data for tables
            tables = tables_init.tables

            if len(tables) == 0:
                format_print_message("Nothing has been found.")
                exit(0)

            colalign = tables_init.colalign
            headers = tables_init.headers

            output_tables = tabulate(tables, headers=headers,
                                     tablefmt="fancy_grid", colalign=colalign)
            print(output_tables)

            # Try to write result to file
            if args.output is not None:
                write_to_file(args.output[0], args.output[1], tables, headers, colalign)

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
