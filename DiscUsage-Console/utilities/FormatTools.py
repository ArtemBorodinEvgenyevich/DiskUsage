import math
from os import path


def convert_size(size_bytes: int):
    if size_bytes == 0:
        return "0B"

    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")

    dimension = int(math.floor(math.log(size_bytes, 1024)))
    power = math.pow(1024, dimension)
    size = round(size_bytes / power, 2)

    return str(f"{size} {size_name[dimension]}")

# TODO
def split_filename(filename: str):
    if len(filename.split(".")) > 2:
        return filename.split('.')[0], '.'.join(filename.split('.')[-2:])
    return path.splitext(filename)


class ASCIIStyle:
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
        return f"\033[{mode};{colour};{background}m"
