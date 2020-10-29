"""
Preprocess Legion Engine Shaders into pure glsl

Usage:
 lgnspre <file> [-D defines ...] [-I includes ...] [options] [-v | -vv | -vvv]

Options:
  -D ...                        additional defines (use = to assign a value)
  -I ...                        additional includes
  -f --format=(1file,nfiles)    output format [default: nfiles]
  -o --output=(file,stdout)     output location [default: file]
  -v                            verbose output level
"""

import re
import sys
from pprint import pprint

from docopt import docopt

from gl_consts import *
from rewrite_compiler import RewriteCompiler
from rewrite_rules.rewrite_includes import Includes
from rewrite_rules.rewrite_layout_location_sugar import LayoutSugar
from rewrite_rules.rewrite_newl_newl_to_newl import NewlNewl2Newl
from rewrite_rules.rewrite_shader_splitter import ShaderSplitter
from rewrite_rules.rewrite_version_defines import VersionToDefines
import vprint
from vprint import vprint0, vprint1, vprint2

lookup = {
    '.vert': GL_LGN_VERTEX_SHADER,
    '.frag': GL_LGN_FRAGMENT_SHADER,
    '.geom': GL_LGN_GEOMETRY_SHADER,
    '.tess-c': GL_LGN_TESS_CONTROL_SHADER,
    '.tess-e': GL_LGN_TESS_EVALUATION_SHADER
}


def armorize(str):
    return "=========== BEGIN SHADER CODE ===========\n" \
         + str \
         + "============ END SHADER CODE ============\n"


def amalgamate(param, filename):
    onesource = ''

    for (source, location) in param:
        match = re.match(r'.*(\..*)$', location)
        if match is not None:
            identifier = lookup.get(match.group(1).lower(), 0)
            onesource += str(identifier) + '\n'
            onesource += str(len(source.encode('utf-8'))) + '\n'
            onesource += source

    return [(onesource, filename + '.onefile')]


def eq_split(s):
    if '=' in s:
        [a, b] = s.split('=')
        return a, b
    else:
        return s, ''


version = "Legion Shader Preprocessor v0.1.0 Alpha 3"


def main():
    vprint1(f"[Bootstrap] Application Started: {version}")
    arguments = docopt(__doc__, version=version)

    vprint.verbosity_level = arguments['-v']

    vprint2(f"[Boostrap] Parsed Arguments:\n{arguments}")

    rewriters = [Includes(arguments['-I']), ShaderSplitter(), VersionToDefines([eq_split(x) for x in arguments['-D']]),
                 LayoutSugar(), NewlNewl2Newl()]

    vprint2(f"[Boostrap] Created Pipeline:\n{rewriters}")

    vprint1(f"[Boostrap] Making Compiler")

    compiler = RewriteCompiler(rewriters)

    location = arguments['<file>']

    try:
        with open(location, 'r') as file:
            vprint2(f"[Boostrap] Loading {location}")
            output = compiler.rewrite_file(file.read(), location)
            vprint1(f"[Boostrap] Ran Compiler, parsing results")

    except Exception as e:
        vprint0(e, file=sys.stderr)
        exit(1)

    if arguments['--format'] == '1file':
        vprint2(f"[Boostrap] Amalgamating Output")
        output = amalgamate(output, location)

    for (source, location) in output:
        if arguments['--output'] == 'file':
            with open(location, 'w') as outfile:
                vprint2(f"[Boostrap] Writing {location}")
                outfile.write(source)
        else:
            if arguments['--format'] != '1file':
                print(f"NAME:{location}")
            print(armorize(source))


if __name__ == '__main__':
    main()
