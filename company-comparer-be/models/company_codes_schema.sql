DROP TABLE IF EXISTS company_codes;

CREATE TABLE company_codes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    popularity INTEGER NOT NULL,
    cik TEXT NOT NULL,
    ticker TEXT NOT NULL,
    company_name TEXT NOT NULL
);