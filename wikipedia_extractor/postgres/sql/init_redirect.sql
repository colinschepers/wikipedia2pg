CREATE TABLE IF NOT EXISTS redirect (
  "from" serial NOT NULL,
  namespace integer NOT NULL DEFAULT 0,
  title text NOT NULL DEFAULT '',
  interwiki text DEFAULT NULL,
  fragment text DEFAULT NULL
);

ALTER TABLE redirect DROP CONSTRAINT IF EXISTS redirect_pkey;
DROP INDEX IF EXISTS redirect_namespace;
DROP INDEX IF EXISTS redirect_title;