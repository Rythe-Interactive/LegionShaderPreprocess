import abc
from typing import List, Dict, Tuple


class RewriteBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def rewrite_source(self, source: str, meta_information: Dict[str, str]) -> List[Tuple[str, Dict[str, str]]]:
        pass
