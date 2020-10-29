from typing import Dict, List, Tuple

from rewrite_rules.rewrite_base import RewriteBase
import re

from vprint import vprint2, vprint1


class VersionToDefines(RewriteBase):

    def __init__(self, defines: List[Tuple[str, str]]):
        self.defines = defines

    def rewrite_source(self, source: str, meta_information: Dict[str, str]) -> List[Tuple[str, Dict[str, str]]]:
        vprint1("[Defines] Rewriter Started")
        vprint2(f"[Defines] I have the following defines to insert:\n{self.defines}")
        vprint2(f"[Defines] The following extra defines have been passed via the pipeline:\n{meta_information['extra_defines'].split(',')}")

        source = re.sub(r"#\s*version\s+([0-9]+)\s*", '#version \\1 \n'
                        + (''.join([f"\n#define {k} {v}" for k, v in self.defines]))
                        + (''.join([f"\n#define {k}" for k in meta_information['extra_defines'].split(',')])
                           if meta_information.get('extra_defines', None) is not None
                           else '')
                        + '\n\n'
                        , source)
        return [(source, meta_information)]
