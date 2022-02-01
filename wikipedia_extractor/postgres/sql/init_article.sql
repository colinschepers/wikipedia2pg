DROP INDEX IF EXISTS article_title;
DROP INDEX IF EXISTS article_redirect;

CREATE TABLE IF NOT EXISTS article (
  id integer NOT NULL,
  title text NOT NULL DEFAULT '',
  text text NOT NULL DEFAULT '',
  redirect text DEFAULT NULL
);