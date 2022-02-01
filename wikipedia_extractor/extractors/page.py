from wikipedia_extractor import Entity, CONFIG
from wikipedia_extractor.extractors.sql import SqlExtractor


class PageExtractor(SqlExtractor):
    @property
    def entity(self):
        return Entity.PAGE

    @property
    def url(self):
        return f"{CONFIG['base_url']}/enwiki-latest-page.sql.gz"
