CREATE TABLE IF NOT EXISTS abstract (
  title text NOT NULL DEFAULT '',
  abstract text NOT NULL DEFAULT ''
);

DROP INDEX IF EXISTS abstract_title;