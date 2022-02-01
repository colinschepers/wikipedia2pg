from abc import ABC, abstractmethod

from wikipedia_extractor import CONFIG
from wikipedia_extractor.postgres import PostgresConnection, get_init_sql, get_finish_sql


class BaseExtractor(ABC):
    def __init__(self, connection: PostgresConnection):
        self.connection = connection
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
    def url(self):
        raise NotImplemented
