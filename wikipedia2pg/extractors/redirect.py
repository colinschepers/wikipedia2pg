from wikipedia2pg import Entity
from wikipedia2pg.extractors.sql import SqlExtractor


class RedirectExtractor(SqlExtractor):
    @property
    def entity(self):
        return Entity.REDIRECT

    @property
    def filename(self):
        return "enwiki-latest-redirect.sql.gz"
