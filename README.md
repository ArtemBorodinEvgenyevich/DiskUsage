# DiskUsage console utility

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

### Description: 

Simple console utility for displaying directory contents and theirs properties.

Shows directory contents:

- file path
- file extension
- file permissions
- file owner
- file access/modify date
- inode
- device id inode resides on
- links number to a file 

Allows sorting from high to low and vice-versa:
- by depth 
- by size

Allows result output in a single file with any table format supported by [tabulate](https://pypi.org/project/tabulate/)

Supports directory tree view output.

### Usage:

Works on OS like: Windows, Linux. (should work on MacOS, haven't tested yet)

Minimal required python version - ``3.7``

Use ``python3 disk_usage.py [PATH-TO-DIR]`` to start search in specified directory. Current path is using, if no given.

Use ``python3 disk_usage.py -h`` to see a detailed info about arguements.

### Docs:

To see docs, run ``host_docs_local.py`` from `/Docs` folder. It will open docs in your system default web browser. 
You can also rebuild docs from source using `build_html.py` (Requires `sphinx sphinx_rtd_theme recommonmark` to be installed)