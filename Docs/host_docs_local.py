import webbrowser
import sys

PATH = "build/html/index.html"
if sys.platform == 'win32':
    PATH = r"build\html\index.html"

webbrowser.open(PATH)