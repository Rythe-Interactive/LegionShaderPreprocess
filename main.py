"""
Preprocess Legion Engine Shaders into pure glsl

Usage:
 lgspre <file> [-D defines ...] [-I includes ...] [options]

Options:
  -D ...                        additional defines (use = to assign a value)
  -I ...                        additional includes
  -f --format=(1file,nfiles)    output format [default: nfiles]
  -o --output=(file,stdout)     output location [default: file]
"""

from rewrite_compiler import RewriteCompiler
from rewrite_rules.rewrite_includes import Includes
from rewrite_rules.rewrite_layout_location_sugar import LayoutSugar
from rewrite_rules.rewrite_newl_newl_to_newl import NewlNewl2Newl
from rewrite_rules.rewrite_shader_splitter import ShaderSplitter
from gl_consts import *
import re

from rewrite_rules.rewrite_version_defines import VersionToDefines
from docopt import docopt

lookup = {
    '.vert': GL_LGN_VERTEX_SHADER,
    '.frag': GL_LGN_FRAGMENT_SHADER,
    '.geom': GL_LGN_GEOMETRY_SHADER,
    '.tess-c': GL_LGN_TESS_CONTROL_SHADER,
    '.tess-e': GL_LGN_TESS_EVALUATION_SHADER
}


def amalgamate(param, filename):
    onesource = ''

    for (source, location) in param:
        match = re.match(r'.*(\..*)$', location)
        if match is not None:
            identifier = lookup.get(match.group(1).lower(), 0)
            onesource += str(identifier) + '\n'
            onesource += str(len(source)) + '\n'
            onesource += source

    return [(onesource, filename + '.onefile')]


def eq_split(s):
    if '=' in s:
        [a, b] = s.split('=')
        return a, b
    else:
        return s, ''


def main():
    arguments = docopt(__doc__, version="0.1.0 Alpha 1")

    rewriters = [Includes(arguments['-I']), ShaderSplitter(), VersionToDefines([eq_split(x) for x in arguments['-D']]),
                 LayoutSugar(), NewlNewl2Newl()]

    compiler = RewriteCompiler(rewriters)

    location = arguments['<file>']

    with open(location, 'r') as file:
        output = compiler.rewrite_file(file.read(), location)

    if arguments['--format'] == '1file':
        output = amalgamate(output,location)

    for (source, location) in output:
        if arguments['--output'] == 'file':
            with open(location, 'w') as outfile:
                # respect -f and -o here
                outfile.write(source)
        else:
            if arguments['--format'] != '1file':
                print(f"NAME:{location}")
            print(source)


if __name__ == '__main__':
    main()
