from typing import Iterable, Any, Tuple

from wikipedia_extractor import Entity


class BaseWriter:
    def write(self, data: Iterable[Tuple[Any]], entity: Entity):
        raise NotImplemented
