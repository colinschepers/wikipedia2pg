ALTER TABLE article
  ADD PRIMARY KEY (id);

CREATE INDEX article_title ON article (title);
CREATE INDEX article_redirect ON article (redirect);