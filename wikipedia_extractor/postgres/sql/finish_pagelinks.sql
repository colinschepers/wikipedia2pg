ALTER TABLE pagelinks
  ADD PRIMARY KEY ("from", namespace, title);

CREATE INDEX pagelinks_from ON pagelinks ("from");
CREATE INDEX pagelinks_title ON pagelinks (title);