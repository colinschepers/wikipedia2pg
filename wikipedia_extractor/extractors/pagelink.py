from wikipedia_extractor import Entity, CONFIG
from wikipedia_extractor.extractors.sql import SqlExtractor


class PagelinkExtractor(SqlExtractor):
    @property
    def entity(self):
        return Entity.PAGELINK

    @property
    def url(self):
        return f"{CONFIG['base_url']}/enwiki-latest-pagelinks.sql.gz"
