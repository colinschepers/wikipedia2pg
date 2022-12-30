# wikipedia2pg

This python tool extracts Wikipedia dumps from your local system or online, and imports them into Postgres. 
It's easy to use and insanely fast. 

## Supported Data

Wikimedia provides public [dumps](http://dumps.wikimedia.org/enwiki/latest) of the wikis' content and related data. 
The dumps are free to download and reuse. Currently, this application only supports the following data, but the code is
set up to be extended with little effort:

| Entity     | Type | File                                                                                                                                          |
|------------|------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| Page       | sql  | [enwiki-latest-page.sql.gz](http://dumps.wikimedia.org/enwiki/latest/enwiki-latest-page.sql.gz)                                               |
| Pagelink   | sql  | [enwiki-latest-pagelinks.sql.gz](http://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pagelinks.sql.gz)                                     |                                                                                                  | Text        |
| Redirect   | sql  | [enwiki-latest-redirect.sql.gz](http://dumps.wikimedia.org/enwiki/latest/enwiki-latest-redirect.sql.gz)                                       |
| Abstract   | xml  | [enwiki-latest-abstract.xml.gz](http://dumps.wikimedia.org/enwiki/latest/enwiki-latest-abstract.xml.gz)                                       |
| Article    | xml  | [enwiki-latest-pages-articles-multistream.xml.bz2](http://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles-multistream.xml.bz2) |

See [this page](https://meta.wikimedia.org/wiki/Data_dumps/What%27s_available_for_download) for a more detailed 
description of each entity.

## Getting Started

Follow the steps below to get started:

1. Install python (>=3.8)
2. Install dependencies: `pip install -r requirements.txt`
3. Optionally, download the dumps to a local directory. If you skip this step, the required files will be downloaded 
automatically when you run the application.
4. Update the Postgres credentials in `config.yaml`. Alternatively, use script arguments to overwrite 
the values (see next section). 

## Usage

Start an extraction from command line using the `run.py` script in the root directory of the repository.

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

To start an extraction from code, please refer to the example below:

```
from wikipedia_extractor import Entity, extract, PostgresConnection

connection = PostgresConnection(host="localhost", port="5432", database="wikipedia",
                                user="user", password="password", schema="public")
extract(connection, Entity.ARTICLE, "\path\to\dumps", drop_table=True)
```
