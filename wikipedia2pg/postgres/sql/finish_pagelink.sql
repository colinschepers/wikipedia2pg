ALTER TABLE pagelink
  ADD PRIMARY KEY ("from", namespace, title);

CREATE INDEX pagelink_from ON pagelink ("from");
CREATE INDEX pagelink_title ON pagelink (title);