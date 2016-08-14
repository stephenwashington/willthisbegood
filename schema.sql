CREATE TABLE IF NOT EXISTS things (
    thing VARCHAR(255) NULL,
    isitgood VARCHAR(5) NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO things values (
    "this website",
    "yes",
    CURRENT_TIMESTAMP
);
