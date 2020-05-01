import argparse
from DiscUsage_Console.DUUtilities.DUFormatTools import format_convert_size

# Dirty hack for windows compatibility... fck'in hate it.
try:
    import pwd
except ImportError:
    import winpwd as pwd


class ArgParser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__()

        self.description = 'DiskUsage [OPTIONS] <SEARCH_DIR>.\n\t' \
                           'Lists files contained in a specified directory.\n\t' \
                           'Generates an ASCII table with file path and its size.\n' \
                           'For more info run `host_docs_local.py` from Docs folder\n'

        self.add_argument("search_dir", nargs='?', help="Files searching directory. If not specified current "
                                                        "directory is used.")

        self.add_argument("-a", "--absolute", action="store_true", help="show absolute path to file")
        self.add_argument("-e", "--extension", type=str, help="show files match specified extension")
        self.add_argument("-l", "--links", action="store_true", help="show number of links to the inode")
        self.add_argument("-i", "--inode", action="store_true", help="show inode number")
        self.add_argument("-d", "--device", action="store_true", help="show device inode resides on")
        self.add_argument("-w", "--owner", action="store_true", help="show file owner")

        self.add_argument("-A", "--adate", action="store_true", help="show date of most recent access")
        self.add_argument("-M", "--mdate", action="store_true", help="show date of most recent content "
                                                                     "modification")


class ArgParserTablesInit:
    def __init__(self, args: argparse.Namespace):

        self.args = args

        self._headers = ["PATH", "SIZE", "EXTENSION"]
        self._colalign = ["left", "center", "center"]
        self._tables = []

    # FIXME: put proper instance name in file param
    def add_table(self, file: 'File'):
        if self.args.extension is not None and file.extension != self.args.extension:
            return

        table = [file.path, format_convert_size(file.size), file.extension]

        if self.args.owner:
            table.append(pwd.getpwuid(file.user_owner).pw_name)
            table.append(pwd.getpwuid(file.group_owner).pw_name)
            if "USER" and "GROUP" not in self._headers:
                self._headers.append("USER")
                self._headers.append("GROUP")
                self._colalign.append("center")
                self._colalign.append("center")
        if self.args.inode:
            table.append(file.inode)
            if "INODE" not in self._headers:
                self._headers.append("INODE")
                self._colalign.append("center")
        if self.args.device:
            table.append(file.device)
            if "DEVICE" not in self._headers:
                self._headers.append("DEVICE")
                self._colalign.append("center")
        if self.args.links:
            table.append(file.links)
            if "LINKS" not in self._headers:
                self._headers.append("LINKS")
                self._colalign.append("center")
        if self.args.adate:
            table.append(file.adate)
            if "ACCESS" not in self._headers:
                self._headers.append("ACCESS")
                self._colalign.append("center")
        if self.args.mdate:
            table.append(file.mdate)
            if "MODIFIED" not in self._headers:
                self._headers.append("MODIFIED")
                self._colalign.append("center")

        self._tables.append(table)

    @property
    def headers(self):
        return self._headers

    @property
    def colalign(self):
        # Convert colalign to tuple requested by "tabulate"
        return tuple(self._colalign)

    @property
    def tables(self):
        return self._tables
