import argparse


class ArgParser(argparse.ArgumentParser):
    def __init__(self, description: str):
        super().__init__(description)

        self.add_argument("search_dir", nargs='?', help="Files searching directory. If not specified current "
                                                        "directory is used.")
        self.add_argument("-a", "--absolute", action="store_true", help="show absolute path to file")
        self.add_argument("-e", "--extension", type=str, help="show files match specified extension")

