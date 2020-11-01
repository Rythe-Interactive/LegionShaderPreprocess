import re
from typing import Dict, List, Tuple

from rewrite_rules.rewrite_base import RewriteBase
from vprint import vprint1


class GeometryInput(RewriteBase):
    rgx_input = re.compile(r"geometry_input\s*\(\s*([^\s][^,\s]*[^\s,)])\s*([,]?[^\)]*)\s*\)")
    rgx_output = re.compile(r"geometry_output\s*\(\s*([^\s][^\)]*[^\s])\s*(\))")

    pattern_input = r"layout(\1\2) in;\n#define __geom_in_\1\n#define __geom_vtxc "
    pattern_output = r"layout(\1) out;"
    vtxc = {
        "points": '1\n',
        "lines": '2\n',
        "lines_adjacency": '4\n',
        "triangles": '3\n',
        "triangles_adjacency": '6\n'
        }

    def rewrite_input_match(self, match):
        return match.expand(self.pattern_input + self.vtxc.get(match.group(1), ''))

    def rewrite_source(self, source: str, meta_information: Dict[str, str]) -> List[Tuple[str, Dict[str, str]]]:
        vprint1("[Geometry-Input] Rewriter started!")
        ret = self.rgx_output.sub(self.pattern_output, source)
        return [(self.rgx_input.sub(self.rewrite_input_match, ret), meta_information)]
