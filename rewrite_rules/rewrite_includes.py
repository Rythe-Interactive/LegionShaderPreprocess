import os
import re
from typing import Dict, List, Tuple

from rewrite_rules.rewrite_base import RewriteBase


def merge_dicts(d1, d2):
    z = d1.copy()
    z.update(d2)
    return z


class Includes(RewriteBase):

    def __init__(self, include_dirs):
        self.include_dirs = include_dirs

    rgx = re.compile(r"\s*#\s*include\s*[\"\<]\s*([A-z\_][A-z0-9_\.\\\/]*)[\"\>]\s*")

    def rewrite_source(self, source: str, meta_information: Dict[str, str]) -> List[Tuple[str, Dict[str, str]]]:
        already_included = meta_information.get('already_included', '').split(',')
        lines = source.splitlines()

        reconstruction = ''

        for line in lines:
            match = self.rgx.match(line)
            if match is not None:
                location = match.group(1)

                file_found = False

                for include_dir in self.include_dirs:
                    test = os.path.join(include_dir, location)
                    if os.path.isfile(test) and os.path.exists(test):
                        if test not in already_included:
                            already_included.append(test)
                            meta_information['already_included'] = ','.join(already_included)
                            with open(test) as include:
                                [(src, _)] = self.rewrite_source(include.read(),
                                                                 merge_dicts(meta_information, {'location': test}))
                                reconstruction += src + '\n'
                                file_found = True
                        break

                if not file_found:
                    raise FileNotFoundError(f"FATAL: The include {location} was not found ")

            else:
                reconstruction += line + '\n'



        return [(reconstruction, meta_information)]
