from copy import deepcopy
from typing import Dict, List, Tuple

from rewrite_rules.rewrite_base import RewriteBase
import re


def commit(sources, sections, line):
    for section in sections:
        sources[section] += line + '\n'


def to_define(current, ending):
    lut = {
        '.vert': 'VERTEX_SHADER',
        '.frag': 'FRAGMENT_SHADER',
        '.geom': 'GEOMETRY_SHADER',
        '.tess-c': 'TESSELATION_CONTROL_SHADER',
        '.tess-e': 'TESSELATION_EVALUATE_SHADER',
        '.faulty': 'SHADER_FAULTY'
    }
    return ','.join(list(filter(None, current.split(',') + [lut[ending]])))


class ShaderSplitter(RewriteBase):
    find_shader_keyword = re.compile(r"shader\(([A-z,\s_]+)\)")
    find_generate_keyword = re.compile(r"generate\(([A-z,\s_]+)\)")

    fault_extension = '.faulty'

    keyword_sections_pairs = {
        'vertex': '.vert',
        'vert': '.vert',
        'fragment': '.frag',
        'frag': '.frag',
        'geometry': '.geom',
        'geom': '.geom',
        'tessellation_control': '.tess-c',
        'tess_ctrl': '.tess-c',
        'tessellation_evaluate': '.tess-e',
        'tess_eval': '.tess-e'
    }

    all_keyword = 'all'
    all_source_types = set([fault_extension] + list(keyword_sections_pairs.values()))
    all_valid_source_types = set(list(keyword_sections_pairs.values()))

    def rewrite_source(self, source: str, meta_information: Dict[str, str]) -> List[Tuple[str, Dict[str, str]]]:

        # split input source into lines
        lines = source.splitlines()

        # prepare output sources
        sources = dict.fromkeys(self.all_source_types, '')

        to_keep = self.all_source_types

        # prepare active sections (by default all sections are enabled
        active_sections = self.all_valid_source_types
        brace_counter = 0
        need_counting = False

        itr = 0
        while itr < len(lines):
            line = lines[itr]

            # make the loop end at some point
            itr += 1

            # check for 'shader(<...>)' keyword
            matches = self.find_shader_keyword.match(line.strip())
            if matches is not None and not need_counting:
                brace_counter = 1 if line.find('{') != -1 else 0
                need_counting = True
                inner = matches.group(1)

                # match keywords to extensions and make sure they are unique
                active_sections = set(
                    self.keyword_sections_pairs.get(x, self.fault_extension) for x in inner.split(','))

                # makes sure that this line does not get put into the output
                continue

            # check for 'generate(<...>)' keyword
            matches = self.find_generate_keyword.match(line.strip())
            if matches is not None:
                inner = matches.group(1)

                # match keywords to extensions and make sure they are unique
                to_keep = set([self.fault_extension] +
                              [self.keyword_sections_pairs.get(x, self.fault_extension) for x in inner.split(',')])

                # makes sure that this line does not get put into the output
                continue

            # check if wee need to count braces
            if need_counting and (line.find('{') != -1 or line.find('}') != -1):

                # swap temp and line
                temp = line
                line = ''

                # for brace counting we need to check basically ever character
                for (idx, char) in enumerate(temp):
                    if char == '{':
                        brace_counter += 1

                        # do not count the first brace of a section
                        if brace_counter == 1:
                            continue

                    elif char == '}':
                        brace_counter -= 1
                        if brace_counter == 0:
                            need_counting = False
                            commit(sources, active_sections, line)
                            active_sections = self.all_valid_source_types
                            lines[itr - 1] = line[idx+1:]
                            itr -= 1

                            continue
                    line += char

            # add the remaining part to the active sources
            commit(sources, active_sections, line.strip())

        res = []

        for keeper in to_keep:
            if sources[keeper] == '':
                continue
            meta = deepcopy(meta_information)
            meta['location'] = meta.get('location', 'error') + keeper
            defs = meta.setdefault('extra_defines', '')
            meta['extra_defines'] += (to_define(defs, keeper))
            res += [(sources[keeper], meta)]

        return res
