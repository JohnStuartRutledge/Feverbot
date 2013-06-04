
CREATE TABLE IF NOT EXISTS scrape_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    spider_name VARCHAR(80) NOT NULL,
    start_time DATETIME NOT NULL,
    finish_time DATETIME NOT NULL,
    finish_reason VARCHAR(80),
    user_agent VARCHAR,
    pages_crawled INTEGER,
    request_bytes INTEGER,
    request_count INTEGER,
    request_count_GET INTEGER,
    response_bytes INTEGER,
    response_status_count_200 INTEGER,
    response_status_count_302 INTEGER,
    memusage_startup INTEGER,
    memusuage_max INTEGER,
    scheduler_memory_enqueued INTEGER
);

CREATE TABLE IF NOT EXISTS scrape_errors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scrape_id INTEGER NOT NULL REFERENCES "scrape_info" ("id"),
    error_count INTEGER
);

CREATE TABLE IF NOT EXISTS fever_business (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    biz_name VARCHAR(80) NOT NULL
);

CREATE TABLE IF NOT EXISTS apt (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scrape_id INTEGER NOT NULL REFERENCES "scrape_info" ("id"),
    biz_id INTEGER NOT NULL REFERENCES "fever_business" ("id"),
    url VARCHAR(80),
    recommended_by INTEGER NOT NULL,
    total_overall_rating REAL,
    overall_parking REAL,
    overall_maintenance REAL,
    overall_construction REAL,
    overall_noise REAL,
    overall_grounds REAL,
    overall_safety REAL,
    overall_office_staff REAL
);

CREATE TABLE IF NOT EXISTS apt_comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scrape_id INTEGER NOT NULL REFERENCES "scrape_info" ("id"),
    biz_id INTEGER NOT NULL REFERENCES "fever_business" ("id"),
    comment_id INTEGER NOT NULL,
    url VARCHAR(300),
    comment_title CHAR,
    comment_username CHAR(60),
    comment_years_stayed CHAR(20),
    comment_message CHAR,
    last_edited CHAR(60)
);

CREATE TABLE IF NOT EXISTS apt_ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scrape_id INTEGER NOT NULL REFERENCES "scrape_info" ("id"),
    biz_id INTEGER NOT NULL REFERENCES "fever_business" ("id"),
    comment_id INTEGER NOT NULL REFERENCES "apt_comments" ("id"),
    overall_rating REAL,
    parking REAL,
    maintenance REAL,
    construction REAL,
    noise REAL,
    grounds REAL,
    safety REAL,
    office_staff REAL
);

CREATE TABLE IF NOT EXISTS apt_replies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scrape_id INTEGER NOT NULL REFERENCES "scrape_info" ("id"),
    biz_id INTEGER NOT NULL REFERENCES "fever_business" ("id"),
    comment_id INTEGER NOT NULL REFERENCES "apt_comments" ("id"),
    reply_id INTEGER NOT NULL,
    reply_name CHAR(60),
    reply CHAR,
    last_edited CHAR(60)
);
