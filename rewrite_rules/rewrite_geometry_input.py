import re
from typing import Dict, List, Tuple
from copy import deepcopy

from common.str_list_util import dict_str_list_append
from rewrite_rules.rewrite_base import RewriteBase
from vprint import vprint1


class GeometryInput(RewriteBase):
    rgx_input = re.compile(r"geometry_input\s*\(\s*([^\s][^,\s]*[^\s,)])\s*([,]?[^\)]*)\s*\)")
    rgx_output = re.compile(r"geometry_output\s*\(\s*([^\s][^\)]*[^\s])\s*(\))")
    extradefines = []
    pattern_input = r"layout(\1\2) in;"
    pattern_output = r"layout(\1) out;"
    vtxc = {
        "points": '1\n',
        "lines": '2\n',
        "lines_adjacency": '4\n',
        "triangles": '3\n',
        "triangles_adjacency": '6\n'
    }

    def rewrite_input_match(self, match):
        self.extradefines += ["_L_geom_in_" + match.group(1)] + ["_L_geom_vtxc " + self.vtxc.get(match.group(1), '3')]
        return match.expand(self.pattern_input)

    def rewrite_source(self, source: str, meta_information: Dict[str, str]) -> List[Tuple[str, Dict[str, str]]]:
        vprint1("[Geometry-Input] Rewriter started!")

        ret = self.rgx_input.sub(self.rewrite_input_match, source)
        meta = deepcopy(meta_information)

        dict_str_list_append(meta, 'extra_defines', self.extradefines)

        return [(self.rgx_output.sub(self.pattern_output, ret), meta)]
