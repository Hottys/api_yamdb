import sqlite3


con = sqlite3.connect(':memory:')

cur = con.cursor()

cur.executescript('''
CREATE TABLE IF NOT EXISTS reviews_user(
    id INTEGER PRIMARY KEY,
    username TEXT,
    email TEXT,
    role TEXT,
    bio TEXT,
    first_name TEXT,
    last_name TEXT
);

CREATE TABLE IF NOT EXISTS reviews_category(
    id INTEGER PRIMARY KEY,
    name TEXT,
    slug TEXT
);

CREATE TABLE IF NOT EXISTS reviews_genre(
    id INTEGER PRIMARY KEY,
    name TEXT,
    slug TEXT
);

CREATE TABLE IF NOT EXISTS reviews_title(
    id INTEGER PRIMARY KEY,
    name TEXT,
    year INTEGER,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES reviews_category (id)
);

CREATE TABLE IF NOT EXISTS reviews_review(
    id INTEGER PRIMARY KEY,
    title_id INTEGER,
    text TEXT,
    author INTEGER,
    score INTEGER,
    pub_date TEXT,
    FOREIGN KEY (title_id) REFERENCES reviews_title (id),
    FOREIGN KEY (author) REFERENCES reviews_user (id)
);

CREATE TABLE IF NOT EXISTS reviews_comment(
    id INTEGER PRIMARY KEY,
    review_id INTEGER,
    text TEXT,
    author INTEGER,
    pub_date TEXT,
    FOREIGN KEY (review_id) REFERENCES reviews_review (id),
    FOREIGN KEY (author) REFERENCES reviews_user (id)
);

CREATE TABLE IF NOT EXISTS reviews_comment(
    id INTEGER PRIMARY KEY,
    title_id INTEGER,
    genre_id INTEGER,
    FOREIGN KEY (title_id) REFERENCES reviews_title(id),
    FOREIGN KEY (genre_id) REFERENCES reviews_genre (id)
);
''')

con.commit()
con.close() 