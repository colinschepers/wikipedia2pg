# wikipedia2pg

## Extract Wikipedia dumps to Postgres

This python tool extracts Wikipedia dumps from your local system or online, and imports them into Postgres. 
It's easy to use and insanely fast. 

### Installation

```
$ pip install -r requirements.txt
```

### Usage

#### Example to start an extraction from code

```
from wikipedia_extractor import Entity, extract
from wikipedia_extractor.postgres import PostgresConnection

pg_kwargs = {host="localhost", port="5432", database="wikipedia", user="user", password="pw", schema="public"} 
connection = PostgresConnection(**pg_kwargs)
extract(connection, Entity.ARTICLE, r"\path\to\dumps", drop_table=True)
```

#### Start an extraction from command line
```
$ python run.py [-h] [--host HOST] [--port PORT] [--database DATABASE] [--user USER] 
                [--password PASSWORD] [--schema SCHEMA] [--path PATH] 
                [--entities [{page,pagelink,redirect,abstract,article} ...]] 
                [--drop-table]

optional arguments:
  -h, --help            Show this help message and exit
  --host HOST           Postgres host
  --port PORT           Postgres port
  --database DATABASE   Postgres database name
  --user USER           Postgres user
  --password PASSWORD   Postgres password
  --schema SCHEMA       Postgres schema
  --path PATH           Path to the Wiki dumps
  --entities [{page,pagelink,redirect,abstract,article} ...]
                        Entities to extract
  --drop-table          Whether to drop table or continue a previous run
```
