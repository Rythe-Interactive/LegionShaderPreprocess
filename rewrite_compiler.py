from rewrite_rules.rewrite_base import RewriteBase
from typing import List, NoReturn, Tuple


class RewriteCompiler:

    def __init__(self, rewriters: List[RewriteBase]):
        self.rewriters = rewriters

    def rewrite_file(self, source: str, location: str) -> List[Tuple[str, str]]:
        """
        Applies all the rewrite-rules specified when this class was constructed, and returns a list of new sources +
        their filenames

        :param source: The input source of the file
        :param location: The file location of the source-file
        :return: new sources + locations
        """

        # generate workspace
        workspaces = [(source, {'location': location})]

        # run all re-writers over the source
        for rewriter in self.rewriters:

            accumulator = []

            for (source, meta) in workspaces:
                accumulator += rewriter.rewrite_source(source, meta)

            workspaces = accumulator

        # transform the workspaces into source, location pairs
        ret = []

        for (source, meta) in workspaces:

            if 'location' not in meta:
                print('Warning! Source without location encountered, skipped!')
                continue

            ret += [(source, meta['location'])]

        return ret
