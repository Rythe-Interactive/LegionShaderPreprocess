import re
from typing import Dict, List, Tuple

from rewrite_rules.rewrite_base import RewriteBase
from vprint import vprint1


class LayoutSugar(RewriteBase):
    rgx = re.compile(r"((?:in|out|uniform)\s+[A-z\_][A-z0-9_\s]*)\s*:\s*([^;]+);")
    pattern = r"layout(location=\2) \1;"

    def rewrite_source(self, source: str, meta_information: Dict[str, str]) -> List[Tuple[str, Dict[str, str]]]:
        vprint1("[Sugar-Layout] Rewriter started!")
        return [(self.rgx.sub(self.pattern, source), meta_information)]
