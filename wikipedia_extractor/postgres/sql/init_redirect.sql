DROP INDEX IF EXISTS redirect_from;
DROP INDEX IF EXISTS redirect_title;

CREATE TABLE IF NOT EXISTS redirect (
  "from" integer NOT NULL DEFAULT 0,
  namespace integer NOT NULL DEFAULT 0,
  title text NOT NULL DEFAULT '',
  interwiki text DEFAULT NULL,
  fragment text DEFAULT NULL
);