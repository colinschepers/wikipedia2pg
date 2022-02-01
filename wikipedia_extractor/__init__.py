from wikipedia_extractor.config import CONFIG
from wikipedia_extractor.entities import Entity
from wikipedia_extractor.extractors.abstract import AbstractExtractor
from wikipedia_extractor.extractors.article import ArticleExtractor
from wikipedia_extractor.extractors.page import PageExtractor
from wikipedia_extractor.extractors.pagelink import PagelinkExtractor
from wikipedia_extractor.extractors.redirect import RedirectExtractor
from wikipedia_extractor.postgres import PostgresConnection

__all__ = [Entity]


def extract(connection: PostgresConnection, entity: Entity):
    if entity == entity.PAGE:
        return PageExtractor(connection).extract()
    elif entity == entity.PAGELINK:
        return PagelinkExtractor(connection).extract()
    elif entity == entity.REDIRECT:
        return RedirectExtractor(connection).extract()
    elif entity == entity.ABSTRACT:
        return AbstractExtractor(connection).extract()
    elif entity == entity.ARTICLE:
        return ArticleExtractor(connection).extract()
    else:
        raise ValueError(f"Invalid entity: {entity.name}")
