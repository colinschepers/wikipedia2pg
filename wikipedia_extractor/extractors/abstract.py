import xml.etree.ElementTree as ET
from typing import Tuple

from wikipedia_extractor import Entity
from wikipedia_extractor.extractors.xml import XmlExtractor


class AbstractExtractor(XmlExtractor):
    def parse_record(self, element: ET.Element) -> Tuple[str, ...]:
        title = str(element.find("title").text).lstrip("Wikipedia: ")
        abstract = str(element.find("abstract").text)
        return title, abstract

    @property
    def record_tag(self):
        return "doc"

    @property
    def entity(self):
        return Entity.ABSTRACT

    @property
    def filename(self):
        return "enwiki-latest-abstract.xml.gz"
