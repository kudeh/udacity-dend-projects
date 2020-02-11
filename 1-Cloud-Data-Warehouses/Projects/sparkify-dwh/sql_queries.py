import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

ARN = config.get('IAM_ROLE', 'ARN')

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
    ts TIMESTAMP,
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
    songplay_id INT IDENTITY(0,1) DISTKEY SORTKEY,
    start_time TIMESTAMP,
    user_id INT,
    level VARCHAR,
    song_id VARCHAR,
    artist_id VARCHAR,
    session_id INT,
    location VARCHAR,
    user_agent VARCHAR
)
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users 
(
    user_id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    gender CHAR(1),
    level VARCHAR
)
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs 
(
    song_id VARCHAR,
    title VARCHAR,
    artist_id VARCHAR,
    year INT,
    duration NUMERIC
)
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists 
(
    artist_id VARCHAR,
    name VARCHAR,
    location VARCHAR,
    latitude NUMERIC,
    longitude NUMERIC
)
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
SELECT TIMESTAMP 'epoch' + es.ts * interval '1 second' AS start_time, 
       es.userId AS user_id, es.level, ss.song_id,
       ss.artist_id, es.sessionId AS session_id, es.location, es.userAgent AS user_agent
INTO
songplays
FROM
(
    SELECT TIMESTAMP 'epoch' + es.ts * interval '1 second' AS start_time, 
       es.userId AS user_id, es.level, ss.song_id,
       ss.artist_id, es.sessionId AS session_id, es.location, es.userAgent AS user_agent
    FROM (
        SELECT * FROM events_staging AS es
        WHERE page = 'NextSong'
        LEFT JOIN
        SELECT * FROM songs_staging AS ss
        ON es.song = ss.title 
        AND es.artist = ss.artist_name
        AND es.length = ss.duration
    ) 
)
""")

user_table_insert = ("""
SELECT userId AS user_id, firstName AS first_name, lastName AS last_name, 
       gender, level 
INTO users 
FROM events_staging
WHERE page='NextSong'
""")

song_table_insert = ("""
SELECT song_id, title, artist_id, year, duration
INTO
songs
FROM songs_staging
""")

artist_table_insert = ("""
SELECT artist_id, artist_name AS name, artist_location AS location, 
       artist_latitude AS latitude, artist_longitude AS longitude
INTO
artists
FROM songs_staging
""")

time_table_insert = ("""
SELECT ts AS start_time, 
       EXTRACT(HOUR FROM ts) AS hour, EXTRACT(DAY FROM ts) AS day, 
       EXTRACT(WEEK FROM ts) AS week, EXTRACT(MONTH FROM ts) AS month, 
       EXTRACT(YEAR FROM ts) AS year, EXTRACT(WEEKDAY FROM ts) AS weekday
INTO
time
WHERE page='NextSong'
FROM 
(SELECT TIMESTAMP 'epoch' + ts * interval '1 second' AS ts FROM events_staging)
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
