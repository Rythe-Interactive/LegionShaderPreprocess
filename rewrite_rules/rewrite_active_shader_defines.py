import re
from typing import Dict, List, Tuple
from copy import deepcopy

from rewrite_rules.rewrite_base import RewriteBase
from vprint import vprint1


class ActiveShaderDefines(RewriteBase):
    find_shader_keyword = re.compile(r"shaders?\(([A-z,\s_]+)\)")
    extradefines = []
    lut = {
        'vertex': 'VERTEX_SHADER_ACTIVE',
        'vert': 'VERTEX_SHADER_ACTIVE',
        'fragment': 'FRAGMENT_SHADER_ACTIVE',
        'frag': 'FRAGMENT_SHADER_ACTIVE',
        'geometry': 'GEOMETRY_SHADER_ACTIVE',
        'geom': 'GEOMETRY_SHADER_ACTIVE',
        'tessellation_control': 'TESSELATION_CONTROL_SHADER_ACTIVE',
        'tess_ctrl': 'TESSELATION_CONTROL_SHADER_ACTIVE',
        'tessellation_evaluate': 'TESSELATION_EVALUATE_SHADER_ACTIVE',
        'tess_eval': 'TESSELATION_EVALUATE_SHADER_ACTIVE'
    }

    def rewrite_source(self, source: str, meta_information: Dict[str, str]) -> List[Tuple[str, Dict[str, str]]]:
        print("[Active-Shader-Defines] Rewriter started!")
        iterator = self.find_shader_keyword.finditer(source)
        for match in iterator:
            for shaderType in match.group(1).split(','):
                key = shaderType.strip()
                if key in self.lut and self.extradefines.count(self.lut[key]) == 0:
                    self.extradefines += [self.lut[key]]
        meta = deepcopy(meta_information)
        defs = meta.setdefault('extra_defines', '')
        meta['extra_defines'] = ','.join(list(filter(None, defs.split(',') + self.extradefines))) + ','
        return [(source, meta)]
