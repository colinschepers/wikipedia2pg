import argparse
from os import getcwd

from wikipedia_extractor import CONFIG, extract_csv, extract_postgres, Entity

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=str, choices=["csv", "postgres"], help="Type of output")
    parser.add_argument("--output-dir", type=str, default=getcwd(), help="Output directory of CSV's")
    parser.add_argument("--host", type=str, default=CONFIG["database"]["host"], help="Postgres host")
    parser.add_argument("--port", type=str, default=CONFIG["database"]["port"], help="Postgres port")
    parser.add_argument("--database", type=str, default=CONFIG["database"]["database"], help="Postgres database name")
    parser.add_argument("--user", type=str, default=CONFIG["database"]["user"], help="Postgres user")
    parser.add_argument("--password", type=str, default=CONFIG["database"]["password"], help="Postgres password")
    parser.add_argument("--schema", type=str, default=CONFIG["database"]["schema"], help="Postgres schema")
    parser.add_argument("--entities", nargs="*", choices=[e.name for e in Entity], help="Entities to extract")
    args = parser.parse_args()

    entities = [Entity[e] for e in args.entities] if args.entities else list(Entity)
    if args.output == "csv":
        extract_csv(args.output_dir, entities=entities)
    elif args.output == "postgres":
        db_args = (args.host, args.port, args.database, args.user, args.password, args.schema)
        extract_postgres(*db_args, entities=entities)
