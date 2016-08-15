CREATE TABLE IF NOT EXISTS things (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    thing TEXT NULL,
    isitgood TEXT NULL,
    sent_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    posted INT NOT NULL DEFAULT 0
);

INSERT INTO things values (
    1,
    "this website",
    "yes",
    "2015-01-01 01:23:45",
    1
);
