CREATE TABLE IF NOT EXISTS page (
  id serial NOT NULL,
  namespace integer NOT NULL DEFAULT 0,
  title text NOT NULL DEFAULT '',
  restrictions text DEFAULT NULL,
  is_redirect smallint NOT NULL,
  is_new smallint NOT NULL,
  random real NOT NULL DEFAULT 0,
  touched text NOT NULL,
  links_updated text DEFAULT NULL,
  latest integer NOT NULL DEFAULT 0,
  len integer NOT NULL DEFAULT 0,
  content_model text DEFAULT NULL,
  lang text DEFAULT NULL
);

ALTER TABLE page DROP CONSTRAINT IF EXISTS page_pkey;
DROP INDEX IF EXISTS page_title;
DROP INDEX IF EXISTS page_is_redirect;