from copy import deepcopy
from typing import Dict, List, Tuple

from rewrite_rules import RewriteBase
import re


class Variant(RewriteBase):
    matcher = re.compile(r"\s*variant\s*\(([A-z_][A-z0-9_,]+)\)")

    def rewrite_source(self, source: str, meta_information: Dict[str, str]) -> List[Tuple[str, Dict[str, str]]]:
        lines = source.splitlines(keepends=True)

        # extract the info we need
        base_name = meta_information.get('location').rsplit('.', maxsplit=1)

        # recreations
        sources = {'default': ""}
        active_variants = None
        delete_next_curly_open = False
        bc = 0

        for line in lines:

            # check if variant keyword was mentioned
            matches = self.matcher.match(source)
            if matches is not None:
                active_variants = matches.group(1).split(',')
                if '{' not in line:
                    delete_next_curly_open = True
                    bc = 1

                # this should not end up in the shaders
                continue

            if delete_next_curly_open and line.startswith('{'):
                delete_next_curly_open = False
                line = line.strip().strip('{')
                bc = 1

            if active_variants is None:
                new_dict = {}
                for k, v in sources.items():
                    new_dict[k] = v + line
                sources = new_dict
            else:
                bc += line.count('{')
                tmp = bc

                bc -= line.count('}')
                if bc <= 0:

                    closing_for_active_variants = '}' * bc + tmp - 1
                    closing_for_everyone = '}' * -bc
                    new_dict = {}

                    for k, v in sources.items():
                        new_dict[k] = v + closing_for_everyone
                        if k in active_variants:
                            new_dict[k] += closing_for_active_variants

                    sources = new_dict

                    active_variants = None
                    continue

                for variant in active_variants:
                    if variant in sources:
                        sources[variant] += line
                    else:
                        sources[variant] = line

        table = []

        for k, v in sources.items():
            if k == "default":
                table += [(v, meta_information)]
            else:
                meta = deepcopy(meta_information)
                meta['location'] = base_name[0] + k + base_name[1]
                table += [(v, meta)]

        return table
