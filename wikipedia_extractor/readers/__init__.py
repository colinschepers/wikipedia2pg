from typing import Iterable, Union, Tuple

from wikipedia_extractor import Entity


class BaseReader:
    def __init__(self, entity: Entity):
        self.entity = entity

    def read(self) -> Iterable[Union[str, Tuple]]:
        raise NotImplemented
