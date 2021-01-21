import hashlib
import re
from typing import List
import os.path

rgx = re.compile(r"\/\/\s!SHA1Marker\s\%\%([a-fA-F0-9]+)\s\*(.+)\%\%")


def sha1sum(contents: bytes) -> str:
    return hashlib.sha1(contents).hexdigest()


def sha1mark(contents: str, location: str) -> str:
    return "// !SHA1Marker %%" + sha1sum(contents.encode('utf-8')) + " *" + location + "%%"


def sha1search(contents: List[str], searchPaths: List[str]) -> bool:
    for line in contents:
        match = rgx.match(line)
        if match is not None:
            sha = match.group(1)
            loc = match.group(2)

            found = False
            for searchPath in searchPaths:
                try:
                    with open(os.path.join(searchPath, loc), "r") as file:
                        contents = file.read()
                        new_sha_sum = sha1sum(contents.encode('utf-8'))
                        if sha == new_sha_sum:
                            found = True
                            break
                        else:
                            print(f"Mismatch for {loc} {sha}!={new_sha_sum}")
                            return False

                except FileNotFoundError:
                    pass

            if not found:
                return False

    return True
