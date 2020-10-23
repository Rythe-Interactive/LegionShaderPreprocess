from pprint import pprint
from typing import Dict, List, Tuple
import re

from rewrite_rules.rewrite_base import RewriteBase


def remove_newlines(source: str) -> Tuple[bool, str]:
    if '\n\n' in source:
        return False, source.replace('\n\n', '\n')
    return True, source


class NewlNewl2Newl(RewriteBase):
    def rewrite_source(self, source: str, meta_information: Dict[str, str]) -> List[Tuple[str, Dict[str, str]]]:
        done = False
        while not done:
            (done, source) = remove_newlines(source)

        return [(source, meta_information)]
