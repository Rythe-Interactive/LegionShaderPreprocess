import os
import re
from typing import Dict, List, Tuple

from common.sha1mark import sha1mark
from rewrite_rules.rewrite_base import RewriteBase
from vprint import vprint1, vprint2


def merge_dicts(d1, d2):
    z = d1.copy()
    z.update(d2)
    return z


class Includes(RewriteBase):

    def __init__(self, include_dirs):
        self.include_dirs = include_dirs

    rgx = re.compile(r"\s*#\s*include\s*[\"\<]\s*([A-z\_][A-z0-9_\.\\\/]*)[\"\>]\s*")

    def rewrite_source(self, source: str, meta_information: Dict[str, str]) -> List[Tuple[str, Dict[str, str]]]:

        vprint1("[Include] Rewriter Started")

        already_included = meta_information.get('already_included', '').split(',')
        lines = source.splitlines()

        reconstruction = ''

        for line in lines:
            match = self.rgx.match(line)
            if match is not None:
                location = match.group(1)

                file_found = False
                vprint2(f"[Include] Searching for {location} in {self.include_dirs}")

                for include_dir in self.include_dirs:

                    vprint1(f"[Include] Searching for {location} in {include_dir}")
                    test = os.path.join(include_dir, location)
                    if os.path.isfile(test) and os.path.exists(test):
                        vprint1("[Include] " + test)
                        if test not in already_included:

                            vprint1(f"[Include] Candidate {test} is valid")
                            already_included.append(test)
                            meta_information['already_included'] = ','.join(already_included)
                            with open(test) as include:
                                vprint2("[Include] Candidate opened")
                                contents = include.read()
                                marker = sha1mark(contents, test)
                                [(src, _)] = self.rewrite_source(contents,
                                                                 merge_dicts(meta_information, {'location': test}))

                                vprint2("[Include] candidate parsed!")
                                reconstruction += marker + '\n' + src + '\n'
                                file_found = True
                        else:
                            vprint1("[Include] Candidate was ignored because it was already included")
                            file_found = True
                        break

                if not file_found:
                    raise FileNotFoundError(f"FATAL: The include {location} was not found ")

            else:
                reconstruction += line + '\n'

        return [(reconstruction, meta_information)]
