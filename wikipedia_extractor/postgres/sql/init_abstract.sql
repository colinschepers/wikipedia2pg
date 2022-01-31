DROP TABLE IF EXISTS abstract;
DROP INDEX IF EXISTS abstract_title;
DROP INDEX IF EXISTS abstract_url_prefix;

CREATE TABLE IF NOT EXISTS abstract (
  title text NOT NULL DEFAULT '',
  url_prefix text NOT NULL DEFAULT '',
  abstract text NOT NULL DEFAULT ''
);