from wikipedia2pg.config import CONFIG
from wikipedia2pg.entities import Entity
from wikipedia2pg.extractors.abstract import AbstractExtractor
from wikipedia2pg.extractors.article import ArticleExtractor
from wikipedia2pg.extractors.page import PageExtractor
from wikipedia2pg.extractors.pagelink import PagelinkExtractor
from wikipedia2pg.extractors.redirect import RedirectExtractor
from wikipedia2pg.postgres import PostgresConnection

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
