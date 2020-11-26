from typing import Dict, List, Tuple
from vprint import vprint1, vprint3

from rewrite_rules import RewriteBase


class Indents(RewriteBase):
    def rewrite_source(self, source: str, meta_information: Dict[str, str]) -> List[Tuple[str, Dict[str, str]]]:
        vprint1("[Indents] Rewriter Started")
        lines = source.splitlines(keepends=True)
        indent_level = 0

        recreation = ""

        for line in lines:
            vprint3(f"[Indents] @level {indent_level}")
            indent_level -= line.count("}")
            recreation += ("\t" * indent_level) + line
            indent_level += line.count("{")

        return [(recreation, meta_information)]
