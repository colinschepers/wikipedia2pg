from typing import Sequence

from wikipedia_extractor.entities import Entity
from wikipedia_extractor.postgres import PostgresConnection
from wikipedia_extractor.readers.sql_reader import SqlReader
from wikipedia_extractor.readers.xml_reader import XmlReader
from wikipedia_extractor.writers import BaseWriter
from wikipedia_extractor.writers.csv_writer import CsvWriter
from wikipedia_extractor.writers.postgres_writer import PostgresWriter


def extract_csv(output_dir: str, entities: Sequence[Entity]):
    _extract(CsvWriter(output_dir), entities)


def extract_postgres(host: str, port: str, database: str, user: str, password: str, schema: str,
                     entities: Sequence[Entity]):
    connection = PostgresConnection(host, port, database, user, password, schema)
    _extract(PostgresWriter(connection), entities)


def _extract(writer: BaseWriter, entities: Sequence[Entity]):
    for entity in entities:
        reader = _get_reader(entity)
        writer.write(reader.read(), entity)


def _get_reader(entity: Entity):
    if entity in (Entity.page, Entity.pagelink, Entity.redirect):
        return SqlReader(entity)
    elif entity in (Entity.abstract, ):
        return XmlReader(entity)
    else:
        raise ValueError()
