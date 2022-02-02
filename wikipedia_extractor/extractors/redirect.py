from wikipedia_extractor import Entity
from wikipedia_extractor.extractors.sql import SqlExtractor


class RedirectExtractor(SqlExtractor):
    @property
    def entity(self):
        return Entity.REDIRECT

    @property
    def filename(self):
        return "enwiki-latest-redirect.sql.gz"
