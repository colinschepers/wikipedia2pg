DROP TABLE IF EXISTS page;
DROP INDEX IF EXISTS page_title;
DROP INDEX IF EXISTS page_is_redirect;

CREATE TABLE IF NOT EXISTS page (
  id integer NOT NULL,
  namespace integer NOT NULL DEFAULT 0,
  title text NOT NULL DEFAULT '',
  restrictions text DEFAULT NULL,
  is_redirect smallint  NOT NULL DEFAULT 0,
  is_new smallint NOT NULL DEFAULT 0,
  random real NOT NULL DEFAULT 0,
  touched text NOT NULL,
  links_updated text DEFAULT NULL,
  latest integer NOT NULL DEFAULT 0,
  len integer NOT NULL DEFAULT 0,
  content_model text DEFAULT NULL,
  lang text DEFAULT NULL
);