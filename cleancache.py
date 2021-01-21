"""
Delete Files that have mismatching SHA1-dependencies

Usage:
 lgncleancache <folder>... [-I includes ...] [options]

Options:
  -I ...                        additional includes
  --dry                         dry run, no files are deleted
"""

import os

from common.sha1mark import sha1search
from docopt import docopt

searchPaths = ['.']


def check(path):
    with open(path) as file:
        return sha1search(file.readlines(), searchPaths)


def visit_folder(folder):
    badfiles = []

    for root, dirs, files in os.walk(folder):
        for file in files:
            if not check(os.path.join(root, file)):
                badfiles += [os.path.join(root, file)]
        for d in dirs:
            badfiles += visit_folder(os.path.join(root, d))

    return badfiles


if __name__ == '__main__':
    arguments = docopt(__doc__)
    searchPaths += arguments['-I']

    for path in arguments['<folder>']:
        for file in visit_folder(path):
            if not arguments['--dry']:
                os.remove(file)

            print("Removed", file)
