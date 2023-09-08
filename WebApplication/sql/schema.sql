-- Create the tables necessary for our project
PRAGMA foreign_keys = ON;

CREATE TABLE Events(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    eventname VARCHAR(40),
    eventorganizer VARCHAR(40),
    address VARCHAR(100)
    start DATETIME,
    end DATETIME
)