import re
from typing import Iterable, Tuple, Union

from wikipedia_extractor.config import CONFIG
from wikipedia_extractor.readers import BaseReader
from wikipedia_extractor.utils import gzip_read_lines


class XmlReader(BaseReader):
    def read(self) -> Iterable[Union[str, Tuple]]:
        url = CONFIG["base_url"] + f"enwiki-latest-{self.entity.value}.xml.gz"

        record = None
        for line in gzip_read_lines(url):
            if line.startswith("<doc>"):
                record = []
            elif match := (
                    re.match("^<title>(?:\w+: )?(.*)</title>$", line) or
                    re.match("^<url>(?:https://en.wikipedia.org/wiki/)(.*)</url>$", line) or
                    re.match("^<abstract>(.*)</abstract>$", line)
            ):
                value = match.group(1).replace("'", "'")
                record.append(f"'{value}'")
            elif re.match("^<(title|url|abstract) />", line):
                record.append("''")
            elif line.startswith("</doc>"):
                yield f"({','.join(record)})"
                record = None
