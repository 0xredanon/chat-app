CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY,
    user TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp TEXT NOT NULL
);
