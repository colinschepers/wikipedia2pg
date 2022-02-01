from os.path import realpath, dirname

from wikipedia_extractor import Entity
from wikipedia_extractor.postgres.connection import PostgresConnection

__all__ = [PostgresConnection]


def get_init_sql(entity: Entity):
    with open(f"{dirname(realpath(__file__))}\sql\init_{entity.value}.sql") as file:
        return file.read()


def get_finish_sql(entity: Entity):
    with open(f"{dirname(realpath(__file__))}\sql\\finish_{entity.value}.sql") as file:
        return file.read()
