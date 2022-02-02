from wikipedia2pg import Entity
from wikipedia2pg.extractors.sql import SqlExtractor


class PageExtractor(SqlExtractor):
    @property
    def entity(self):
        return Entity.PAGE

    @property
    def filename(self):
        return "enwiki-latest-page.sql.gz"
