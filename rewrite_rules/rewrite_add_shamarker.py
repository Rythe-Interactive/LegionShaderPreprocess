from typing import Dict, List, Tuple

from rewrite_rules import RewriteBase
from common import sha1mark


class AddShaMarker(RewriteBase):
    def rewrite_source(self, source: str, meta_information: Dict[str, str]) -> List[Tuple[str, Dict[str, str]]]:
        marker = sha1mark.sha1mark(source, meta_information['location'])
        return [(marker + '\n' + source, meta_information)]
