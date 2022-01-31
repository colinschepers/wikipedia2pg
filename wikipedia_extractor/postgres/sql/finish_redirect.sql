ALTER TABLE redirect
  ADD PRIMARY KEY ("from");

CREATE INDEX redirect_namespace ON redirect (namespace);
CREATE INDEX redirect_title ON redirect (title);