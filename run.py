import argparse

from wikipedia2pg import CONFIG, Entity, extract, PostgresConnection

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default=CONFIG["database"]["host"], help="Postgres host")
    parser.add_argument("--port", type=str, default=CONFIG["database"]["port"], help="Postgres port")
    parser.add_argument("--database", type=str, default=CONFIG["database"]["database"], help="Postgres database name")
    parser.add_argument("--user", type=str, default=CONFIG["database"]["user"], help="Postgres user")
    parser.add_argument("--password", type=str, default=CONFIG["database"]["password"], help="Postgres password")
    parser.add_argument("--schema", type=str, default=CONFIG["database"]["schema"], help="Postgres schema")
    parser.add_argument("--path", type=str, default="", help="Path to the Wiki dumps")
    parser.add_argument("--entities", nargs="*", choices=[e.value for e in Entity], help="Entities to extract")
    parser.add_argument("--drop-table", action='store_true', help="Whether to drop table or continue a previous run")
    args = parser.parse_args()

    connection = PostgresConnection(args.host, args.port, args.database, args.user, args.password, args.schema)
    entities = list(map(Entity, args.entities) if args.entities else Entity)

    for entity in entities:
        extract(connection, entity, args.path, bool(args.drop_table))
