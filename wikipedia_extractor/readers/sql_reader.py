import re
from typing import Iterable, Tuple, Union

from wikipedia_extractor.config import CONFIG
from wikipedia_extractor.readers import BaseReader
from wikipedia_extractor.utils import gzip_read_lines


class SqlReader(BaseReader):
    def read(self) -> Iterable[Union[str, Tuple]]:
        url = CONFIG["base_url"] + f"enwiki-latest-{self.entity.value}.sql.gz"

        for line in gzip_read_lines(url):
            if not line.startswith("INSERT"):
                continue

            line = re.sub(r"^INSERT INTO \S+ VALUES\s*", "", line)

            start_idx = 0
            for match in re.finditer(r"\),\(", line):
                end_idx = match.start() + 1
                yield line[start_idx:end_idx]
                start_idx = match.end() - 1
