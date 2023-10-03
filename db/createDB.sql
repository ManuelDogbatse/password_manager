CREATE TABLE password(
    id SERIAL PRIMARY KEY,
    website TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL UNIQUE
);

CREATE TABLE master_password(
	password TEXT
);

INSERT INTO master_password
VALUES (NULL);