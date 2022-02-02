ALTER TABLE page
  ADD PRIMARY KEY (id);

CREATE INDEX page_title ON page (title);
CREATE INDEX page_is_redirect ON page (is_redirect);