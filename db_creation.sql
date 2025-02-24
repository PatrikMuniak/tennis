

CREATE TABLE requests (
    dt DATETIME DEFAULT CURRENT_TIMESTAMP,
    venue VARCHAR(40),
    content TEXT
);
ALTER TABLE requests ADD COLUMN venue_name VARCHAR(40);
ALTER TABLE requests RENAME COLUMN venue TO venue_id;
ALTER TABLE requests DROP COLUMN venue_name;

CREATE TABLE sessions (
    request_date BIGINT,
    court_name VARCHAR(80),
    date BIGINT,
    sessionName VARCHAR(80),
    start INT,
    end INT,
    venue_name VARCHAR(80),
    venue_id VARCHAR(40),
    booking_url VARCHAR(160)
);

