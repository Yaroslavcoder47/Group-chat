CREATE TABLE IF NOT EXISTS Users(
    id smallserial PRIMARY KEY,
    email varchar(40),
    username varchar(15),
    created_at timestamp
);

CREATE TABLE IF NOT EXISTS Email_codes(
    id smallserial PRIMARY KEY,
    email varchar(40),
    hashed_code text NOT NULL,
    verified boolean,
    created_at timestamp
);

CREATE TABLE IF NOT EXISTS Refresh_tokens(
    id smallserial PRIMARY KEY,
    user_id smallserial REFERENCES Users (id) ON DELETE CASCADE,
    hashed_token text,
    expires_at timestamp,
    created_at timestamp,
    revoked boolean
);