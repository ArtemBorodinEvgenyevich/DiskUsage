# -*- coding: utf-8 -*-

from tabulate import tabulate
from DiscUsage_Console.DUCore.DUSpinner import Spinner
from DiscUsage_Console.DUCore.DUFileCrawler import FileCrawler
from DiscUsage_Console.DUCore.DUArgParser import ArgParser
from DiscUsage_Console.DUUtilities.DUFormatTools import *

import sys

# TODO: remove
# Dirty hack for windows compatibility... fck'in hate it.
try:
    import pwd
except ImportError:
    import winpwd as pwd


def main() -> None:
    # Init argument parser, threads and tables
    parser = ArgParser()
    args = parser.parse_args()
    tables = []
    crawler = FileCrawler(args=args)
    waiting_ico = Spinner()

    # Init basic table headers and alignment. Requirement for "tabulate" module
    headers, colalign = format_columns(args=args)

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

            # TODO Add content after creating a column.
            # TODO Separate from main somehow...
            # Check if additional columns are needed
            if args.owner:
                table.append(pwd.getpwuid(file.user_owner).pw_name)
                table.append(pwd.getpwuid(file.group_owner).pw_name)
            if args.inode:
                table.append(file.inode)
            if args.device:
                table.append(file.device)
            if args.links:
                table.append(file.links)

            if args.adate:
                table.append(file.adate)
            if args.mdate:
                table.append(file.mdate)

            tables.append(table)

        # Check for internal tabulate function error.
        # IndexError raised in case no elements in tables or invalid data passed.
        try:
            # Convert colalign to tuple requested by "tabulate"
            output_tables = tabulate(tables, headers=headers, tablefmt="fancy_grid",
                                     colalign=tuple(colalign))
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
