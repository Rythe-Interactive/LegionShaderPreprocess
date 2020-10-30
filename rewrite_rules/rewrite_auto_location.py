import re
from typing import Dict, List, Tuple

from rewrite_rules.rewrite_base import RewriteBase
from vprint import vprint1


class LocationAuto(RewriteBase):
    rgx = re.compile(r"layout\((location\s*=\s*auto\s*,?)\s*(.*)\)")
    pattern = r"layout(\2);"

    def rewrite_source(self, source: str, meta_information: Dict[str, str]) -> List[Tuple[str, Dict[str, str]]]:
        vprint1("[Location-Auto] Rewriter started!")
        return [(self.rgx.sub(self.pattern, source), meta_information)]
