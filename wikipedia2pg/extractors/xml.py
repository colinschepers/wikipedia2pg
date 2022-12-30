import xml.etree.ElementTree as ET
from abc import abstractmethod
from itertools import islice
from typing import Iterable, Tuple

from psycopg2.extras import execute_values

from wikipedia2pg.extractors import BaseExtractor
from wikipedia2pg.utils import read_compressed, get_count, chunks


class XmlExtractor(BaseExtractor):
    @property
    @abstractmethod
    def record_tag(self):
        raise NotImplemented

    @abstractmethod
    def parse_record(self, element: ET.Element) -> Tuple[str, ...]:
        raise NotImplemented

    def insert_data(self):
        with self.connection.cursor() as cursor:
            count = get_count(cursor, self.entity)
            records = islice(self._get_records(), count, None)
            for chunk in chunks(records, self.insert_batch_size):
                insert_query = f"INSERT INTO {self.entity.value} VALUES %s"
                execute_values(cursor, insert_query, chunk, page_size=self.insert_batch_size)
                self.connection.commit()

    def _get_records(self) -> Iterable[Tuple[str, ...]]:
        record = None
        for line in read_compressed(self.path, self.filename):
            line = line.lstrip()

            if record is not None:
                record.append(line)

            if line.startswith(f"<{self.record_tag}>"):
                record = [line]
            elif line.startswith(f"</{self.record_tag}>"):
                root = ET.fromstring("".join(record))
                yield self.parse_record(root)
                record = None
