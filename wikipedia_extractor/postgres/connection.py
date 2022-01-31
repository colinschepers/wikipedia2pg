import contextlib

import psycopg2


class PostgresConnection:
    def __init__(self, host: str, port: str, database: str, user: str, password: str, schema: str):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.schema = schema
        self._connection = None

    @contextlib.contextmanager
    def cursor(self):
        yield self.connection.cursor()
        self.connection.commit()

    @property
    def connection(self):
        if not self._connection:
            self._connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.database,
                user=self.user,
                password=self.password,
                options=f'-c search_path={self.schema}'
            )
        return self._connection
