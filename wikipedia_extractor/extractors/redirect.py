from wikipedia_extractor import Entity, CONFIG
from wikipedia_extractor.extractors.sql import SqlExtractor


class RedirectExtractor(SqlExtractor):
    @property
    def entity(self):
        return Entity.REDIRECT

    @property
    def url(self):
        return f"{CONFIG['base_url']}/enwiki-latest-redirect.sql.gz"
