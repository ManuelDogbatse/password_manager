CREATE TABLE login_cred(
    id SERIAL PRIMARY KEY,
    website TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL UNIQUE
);

CREATE TABLE auth_config(
	master_password TEXT DEFAULT NULL
);

INSERT INTO auth_config
VALUES (NULL);