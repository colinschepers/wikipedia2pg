from wikipedia2pg import Entity
from wikipedia2pg.extractors.sql import SqlExtractor


class PagelinkExtractor(SqlExtractor):
    @property
    def entity(self):
        return Entity.PAGELINK

    @property
    def filename(self):
        return "enwiki-latest-pagelinks.sql.gz"
