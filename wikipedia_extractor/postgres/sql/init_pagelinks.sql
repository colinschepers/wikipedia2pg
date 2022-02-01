DROP INDEX IF EXISTS pagelinks_from;
DROP INDEX IF EXISTS pagelinks_title;

CREATE TABLE IF NOT EXISTS pagelinks (
  "from" integer NOT NULL DEFAULT 0,
  namespace integer NOT NULL DEFAULT 0,
  title text NOT NULL DEFAULT '',
  from_namespace integer NOT NULL DEFAULT 0
);