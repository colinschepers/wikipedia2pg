from abc import ABC, abstractmethod

from wikipedia2pg import CONFIG
from wikipedia2pg.postgres import PostgresConnection, get_init_sql, get_finish_sql


class BaseExtractor(ABC):
    def __init__(self, connection: PostgresConnection, path: str):
        self.connection = connection
        self.path = path
        self.insert_batch_size = CONFIG["insert_batch_size"]

    def extract(self):
        with self.connection.cursor() as cursor:
            cursor.execute(get_init_sql(self.entity))
        self.insert_data()
        with self.connection.cursor() as cursor:
            cursor.execute(get_finish_sql(self.entity))

    @abstractmethod
    def insert_data(self):
        raise NotImplemented

    @property
    @abstractmethod
    def entity(self):
        raise NotImplemented

    @property
    @abstractmethod
    def filename(self):
        raise NotImplemented
