CREATE TABLE IF NOT EXISTS article (
  id serial NOT NULL,
  title text NOT NULL DEFAULT '',
  text text NOT NULL DEFAULT '',
  redirect text DEFAULT NULL
);

ALTER TABLE article DROP CONSTRAINT IF EXISTS article_pkey;
DROP INDEX IF EXISTS article_title;
DROP INDEX IF EXISTS article_redirect;