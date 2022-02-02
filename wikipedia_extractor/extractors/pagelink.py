from wikipedia_extractor import Entity
from wikipedia_extractor.extractors.sql import SqlExtractor


class PagelinkExtractor(SqlExtractor):
    @property
    def entity(self):
        return Entity.PAGELINK

    @property
    def filename(self):
        return "enwiki-latest-pagelinks.sql.gz"
