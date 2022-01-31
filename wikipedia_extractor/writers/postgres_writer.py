from os.path import dirname, realpath
from sqlite3 import Cursor
from typing import Tuple, Any, Iterable, Union

from wikipedia_extractor import Entity
from wikipedia_extractor.config import CONFIG
from wikipedia_extractor.postgres import PostgresConnection
from wikipedia_extractor.utils import chunks
from wikipedia_extractor.writers import BaseWriter


class PostgresWriter(BaseWriter):
    def __init__(self, connection: PostgresConnection, insert_batch_size=None):
        self.connection = connection
        self.insert_batch_size = insert_batch_size or CONFIG["insert_batch_size"]

    def write(self, data: Iterable[Union[str, Tuple]], entity: Entity):
        with self.connection.cursor() as cursor:
            cursor.execute(self._get_init_sql(entity))
            self._insert_data(data, entity, cursor)
            cursor.execute(self._get_finish_sql(entity))

    def _insert_data(self, data: Iterable[Union[str, Tuple]], entity: Entity, cursor: Cursor):
        for records in chunks(map(PostgresWriter._parse_record, data), self.insert_batch_size):
            sql = f"INSERT INTO {entity.value} VALUES {','.join(records)};"
            sql = sql.replace("\\\\", chr(27)).replace("\\'", "''").replace(chr(27), "\\")
            cursor.execute(sql)

    @staticmethod
    def _parse_record(record: Union[str, Tuple]) -> str:
        if isinstance(record, str):
            return record
        elif isinstance(record, Tuple):
            return f"({','.join(PostgresWriter._parse_field(field) for field in record)})"

    @staticmethod
    def _parse_field(field: Any) -> str:
        if field is None:
            return 'NULL'
        elif isinstance(field, str):
            return f"'{field}'"
        return str(field)

    @staticmethod
    def _get_init_sql(entity: Entity):
        with open(f"{dirname(realpath(__file__))}\..\postgres\\sql\init_{entity.value}.sql") as file:
            return file.read()

    @staticmethod
    def _get_finish_sql(entity: Entity):
        with open(f"{dirname(realpath(__file__))}\..\postgres\\sql\\finish_{entity.value}.sql") as file:
            return file.read()
