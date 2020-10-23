import re
from typing import Dict, List, Tuple

from rewrite_rules.rewrite_base import RewriteBase


class LayoutSugar(RewriteBase):
    rgx = re.compile(r"((?:in|out|uniform)\s+[A-z\_][A-z0-9_]*\s+[A-z\_][A-z0-9_]*)\s*:\s*(.+);")
    pattern = r"layout(location=\2) \1;"

    def rewrite_source(self, source: str, meta_information: Dict[str, str]) -> List[Tuple[str, Dict[str, str]]]:
        return [(self.rgx.sub(self.pattern, source), meta_information)]
