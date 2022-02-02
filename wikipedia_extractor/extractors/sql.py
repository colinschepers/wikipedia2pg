import os
import re
from itertools import islice
from pathlib import Path
from typing import Iterable

from wikipedia_extractor.extractors import BaseExtractor
from wikipedia_extractor.utils import read_compressed, chunks, get_count


class SqlExtractor(BaseExtractor):
    def insert_data(self):
        with self.connection.cursor() as cursor:
            count = get_count(cursor, self.entity)
            records = islice(self._get_records(), count, None)
            for chunk in chunks(records, self.insert_batch_size):
                sql = f"INSERT INTO {self.entity.value} VALUES {','.join(chunk)};"
                cursor.execute(sql)
                self.connection.commit()

    def _get_records(self) -> Iterable[str]:
        for line in read_compressed(self.path, self.filename):
            if not line.startswith("INSERT"):
                continue

            line = re.sub(r"^INSERT INTO \S+ VALUES\s*", "", line)\
                .replace("\\\\", chr(27)).replace("\\'", "''").replace(chr(27), "\\")

            start_idx = 0
            for match in re.finditer(r"\),\(", line):
                end_idx = match.start() + 1
                yield line[start_idx:end_idx]
                start_idx = match.end() - 1
