DROP TABLE IF EXISTS note;
DROP TABLE IF EXISTS user;

CREATE TABLE note (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    tag TEXT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    preview TEXT NOT NULL,
    content TEXT NOT NULL
);

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT 
);

-- INSERT INTO note (title, tag, content) VALUES ('title', 'windows', 'some content');