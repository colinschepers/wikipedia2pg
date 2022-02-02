from wikipedia_extractor import Entity
from wikipedia_extractor.extractors.sql import SqlExtractor


class PageExtractor(SqlExtractor):
    @property
    def entity(self):
        return Entity.PAGE

    @property
    def filename(self):
        return "enwiki-latest-page.sql.gz"
