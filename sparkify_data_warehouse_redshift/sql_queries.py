import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

ARN = config.get('IAM_ROLE', 'ARN')
LOG_DATA = config.get('S3', 'LOG_DATA')
LOG_JSONPATH = config.get('S3', 'LOG_JSONPATH')
SONG_DATA = config.get('S3', 'SONG_DATA')

# DROP TABLES
staging_events_table_drop = "DROP TABLE IF EXISTS events_staging"
staging_songs_table_drop = "DROP TABLE IF EXISTS songs_staging"
songplay_table_drop = "DROP TABLE IF EXISTS songplays CASCADE"
user_table_drop = "DROP TABLE IF EXISTS users CASCADE"
song_table_drop = "DROP TABLE IF EXISTS songs CASCADE"
artist_table_drop = "DROP TABLE IF EXISTS artists CASCADE"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES
staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS events_staging
(
    artist VARCHAR,
    auth VARCHAR,
    firstName VARCHAR,
    gender CHAR(1),
    itemInSession INT,
    lastName VARCHAR,
    length NUMERIC,
    level VARCHAR,
    location VARCHAR,
    method VARCHAR,
    page VARCHAR,
    registration NUMERIC,
    sessionId INT,
    song VARCHAR,
    status INT,
    ts BIGINT,
    userAgent VARCHAR,
    userId INT
)
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS songs_staging 
(
    num_songs INT,
    artist_id VARCHAR,
    artist_latitude NUMERIC,
    artist_longitude NUMERIC,
    artist_location VARCHAR,
    artist_name VARCHAR,
    song_id VARCHAR,
    title VARCHAR,
    duration NUMERIC,
    year INT
)
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays 
(
    songplay_id INT IDENTITY(0,1) SORTKEY PRIMARY KEY,
    start_time TIMESTAMP,
    user_id INT REFERENCES users(user_id) DISTKEY,
    level VARCHAR,
    song_id VARCHAR REFERENCES songs(song_id),
    artist_id VARCHAR REFERENCES artists(artist_id),
    session_id INT,
    location VARCHAR,
    user_agent VARCHAR
)
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users 
(
    user_id INT SORTKEY PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR,
    gender CHAR(1),
    level VARCHAR
)
DISTSTYLE ALL
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs 
(
    song_id VARCHAR SORTKEY PRIMARY KEY,
    title VARCHAR,
    artist_id VARCHAR,
    year INT,
    duration NUMERIC
)
DISTSTYLE ALL
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists 
(
    artist_id VARCHAR SORTKEY PRIMARY KEY,
    name VARCHAR,
    location VARCHAR,
    latitude NUMERIC,
    longitude NUMERIC
)
DISTSTYLE ALL
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time 
(
    start_time TIMESTAMP SORTKEY,
    hour INT,
    day INT,
    week INT,
    month INT,
    year INT,
    weekday INT
)
DISTSTYLE ALL
""")

# STAGING TABLES
staging_events_copy = ("""
COPY events_staging
FROM {}
IAM_ROLE {}
FORMAT AS JSON {}
""").format(LOG_DATA, ARN, LOG_JSONPATH)

staging_songs_copy = ("""
COPY songs_staging
FROM {}
IAM_ROLE {}
FORMAT AS JSON 'auto'
""").format(SONG_DATA, ARN)

# FINAL TABLES
songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
(
    SELECT TIMESTAMP 'epoch' + es.ts/1000 * interval '1 second' AS start_time, 
           es.userId AS user_id, es.level, ss.song_id,
           ss.artist_id, es.sessionId AS session_id, es.location, es.userAgent AS user_agent
    FROM (
            (SELECT ts, userId, level, sessionId, location, userAgent, song, artist, length FROM events_staging
            WHERE page = 'NextSong')  AS es
        JOIN
            (SELECT song_id, artist_id, title, artist_name, duration FROM songs_staging) AS ss
        ON es.song = ss.title 
        AND es.artist = ss.artist_name
        AND es.length = ss.duration
    ) 
)
""")

user_table_insert = ("""
INSERT INTO users 
(
  SELECT user_id, first_name, last_name, gender, level FROM 
    (SELECT userId AS user_id, firstName AS first_name, lastName AS last_name, gender, level, ts
     FROM events_staging
     WHERE page='NextSong')
)

""")

song_table_insert = ("""
INSERT INTO songs
(
    SELECT song_id, title, artist_id, year, duration
    FROM songs_staging
)
""")

artist_table_insert = ("""
INSERT INTO artists
(
    SELECT artist_id, artist_name AS name, artist_location AS location, 
           artist_latitude AS latitude, artist_longitude AS longitude
    FROM songs_staging
)
""")

time_table_insert = ("""
INSERT INTO time
(
    SELECT ts AS start_time, 
       EXTRACT(HOUR FROM ts) AS hour, EXTRACT(DAY FROM ts) AS day, 
       EXTRACT(WEEK FROM ts) AS week, EXTRACT(MONTH FROM ts) AS month, 
       EXTRACT(YEAR FROM ts) AS year, EXTRACT(WEEKDAY FROM ts) AS weekday
    FROM
    (SELECT TIMESTAMP 'epoch' + ts/1000 * interval '1 second' AS ts 
     FROM events_staging
     WHERE page='NextSong')
)
""")

# QUERY LISTS
create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
