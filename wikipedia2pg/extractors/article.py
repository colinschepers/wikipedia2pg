import xml.etree.ElementTree as ET
from typing import Tuple

from wikipedia2pg import Entity
from wikipedia2pg.extractors.xml import XmlExtractor


class ArticleExtractor(XmlExtractor):
    @property
    def entity(self):
        return Entity.ARTICLE

    @property
    def filename(self):
        return "enwiki-latest-pages-articles-multistream.xml.bz2"

    @property
    def record_tag(self):
        return "page"

    def parse_record(self, element: ET.Element) -> Tuple[str, ...]:
        identifier = str(element.find("id").text)
        title = str(element.find("title").text)
        text = str(element.find("revision/text").text)
        redirect = element.find("redirect")
        redirect = redirect.get("title") if redirect is not None else None
        return identifier, title, text, redirect
