from wikipedia_extractor.config import CONFIG
from wikipedia_extractor.entities import Entity
from wikipedia_extractor.extractors.abstract import AbstractExtractor
from wikipedia_extractor.extractors.article import ArticleExtractor
from wikipedia_extractor.extractors.page import PageExtractor
from wikipedia_extractor.extractors.pagelink import PagelinkExtractor
from wikipedia_extractor.extractors.redirect import RedirectExtractor
from wikipedia_extractor.postgres import PostgresConnection

__all__ = [CONFIG, Entity, PostgresConnection]


def extract(connection: PostgresConnection, entity: Entity, path: str = "", drop_table: bool = False):
    if drop_table:
        with connection.cursor() as cursor:
            cursor.execute(f"DROP TABLE IF EXISTS {entity.value};")

    if entity == entity.PAGE:
        return PageExtractor(connection, path).extract()
    elif entity == entity.PAGELINK:
        return PagelinkExtractor(connection, path).extract()
    elif entity == entity.REDIRECT:
        return RedirectExtractor(connection, path).extract()
    elif entity == entity.ABSTRACT:
        return AbstractExtractor(connection, path).extract()
    elif entity == entity.ARTICLE:
        return ArticleExtractor(connection, path).extract()
    else:
        raise ValueError(f"Invalid entity: {entity.name}")
