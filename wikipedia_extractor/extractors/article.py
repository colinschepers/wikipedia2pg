import xml.etree.ElementTree as ET
from typing import Tuple

from wikipedia_extractor import Entity, CONFIG
from wikipedia_extractor.extractors.xml import XmlExtractor


class ArticleExtractor(XmlExtractor):
    def parse_record(self, element: ET.Element) -> Tuple[str, ...]:
        identifier = str(element.find("id").text)
        title = str(element.find("title").text)
        text = str(element.find("revision/text").text)
        redirect = element.find("redirect")
        redirect = redirect.get("title") if redirect is not None else None
        return identifier, title, text, redirect

    @property
    def record_tag(self):
        return "page"

    @property
    def entity(self):
        return Entity.ARTICLE

    @property
    def url(self):
        return f"{CONFIG['base_url']}/enwiki-latest-pages-articles-multistream.xml.bz2"
