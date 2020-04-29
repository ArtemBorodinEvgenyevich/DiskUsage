from tabulate import tabulate
from FileCrawler import FileCrawler
from utilities.FormatTools import convert_size, ASCIIStyle
from Spinner import Spinner
import sys, os


def check_path(search_path: str):
    if not os.path.exists(search_path):
        raise FileNotFoundError

    return search_path

if __name__ == '__main__':

    path = os.path.abspath(os.path.curdir)
    args = sys.argv

    if len(args) > 1:
        try:
            path = check_path(args[1])
        except FileNotFoundError:
            print(f"{ASCIIStyle.RED}--------------------------------- ")
            print("Error! ")
            print("Specified folder does not exist!")
            print("Try once again.")
            print(f"---------------------------------{ASCIIStyle.RESET}")
            exit(0)

    tables = []

    crawler = FileCrawler(root=path)
    waiting_ico = Spinner()

    waiting_ico.start()
    files = [file for file in crawler.get_files()]
    waiting_ico.stop()

    for file in files:
        table = [file.path, convert_size(file.size), file.extension]
        tables.append(table)

    headers = [f"PATH", "SIZE", "EXTENSION"]
    print(tabulate(tables, headers=headers, tablefmt="fancy_grid", colalign=("left", "center", "center")))
