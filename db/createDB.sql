CREATE TABLE password(
    id SERIAL PRIMARY KEY,
    website TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL UNIQUE
);