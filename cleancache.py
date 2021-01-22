"""
Delete Files that have mismatching SHA1-dependencies

Usage:
 lgncleancache <folder>... [-I includes ...] [options] [--filter=<ext>]

Options:
  -I ...                        additional includes
  --dry                         dry run, no files are deleted
  --filter=<ext>                Filter on which extension to check
"""

import os
from typing import Optional

from common.sha1mark import sha1search
from docopt import docopt

searchPaths = ['.']


def check(path):
    with open(path) as file:
        return sha1search(file.readlines(), searchPaths)


def visit_folder(folder, ext: Optional[str]):
    badfiles = []

    for root, dirs, files in os.walk(folder):
        for file in files:
            if ext is not None:
                if not file.endswith(ext):
                    continue

            if not check(os.path.join(root, file)):
                badfiles += [os.path.join(root, file)]
        for d in dirs:
            badfiles += visit_folder(os.path.join(root, d), ext)

    return badfiles


if __name__ == '__main__':
    arguments = docopt(__doc__)
    searchPaths += arguments['-I']

    for path in arguments['<folder>']:
        for file in visit_folder(path,arguments['--filter']):
            if not arguments['--dry']:
                os.remove(file)

            print("Removed", file)
