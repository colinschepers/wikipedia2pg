CREATE TABLE IF NOT EXISTS pagelink (
  "from" serial NOT NULL,
  namespace integer NOT NULL DEFAULT 0,
  title text NOT NULL DEFAULT '',
  from_namespace integer NOT NULL DEFAULT 0
);

ALTER TABLE pagelink DROP CONSTRAINT IF EXISTS pagelink_pkey;
DROP INDEX IF EXISTS pagelink_from;
DROP INDEX IF EXISTS pagelink_title;