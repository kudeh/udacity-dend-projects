"""
All Queries Used for data modeling
"""

# DROP TABLES
session_item_drop = """DROP TABLE IF EXISTS session_item"""
user_session_drop = """DROP TABLE IF EXISTS user_session"""
song_user_drop = """DROP TABLE IF EXISTS song_user"""


# CREATE TABLES
session_item_create = """CREATE TABLE IF NOT EXISTS session_item
                        (session_id INT, session_item_id INT, artist_name VARCHAR, song_title VARCHAR, song_length DOUBLE,
                        PRIMARY KEY (session_id, session_item_id))
                    """
user_session_create = """CREATE TABLE IF NOT EXISTS user_session
                        (user_id INT, session_id INT, session_item_id INT, artist_name VARCHAR, first_name VARCHAR, last_name VARCHAR, song_title VARCHAR,
                        PRIMARY KEY (user_id, session_id, session_item_id))
                     """
song_user_create = """CREATE TABLE IF NOT EXISTS song_user
                     (song_title VARCHAR, first_name VARCHAR, last_name VARCHAR,
                     PRIMARY KEY (song_title))
                  """


# INSERT QUERIES
session_item_insert = """INSERT INTO session_item (session_id, session_item_id, artist_name, song_title, song_length)
                         VALUES (%s, %s, %s, %s, %s)
                      """
user_session_insert = """INSERT INTO user_session (user_id, session_id, session_item_id, artist_name, first_name, last_name, song_title)
                         VALUES (%s, %s, %s, %s, %s, %s, %s)
                      """
song_user_insert = """INSERT INTO song_user (song_title, first_name, last_name)
                      VALUES (%s, %s, %s)"""


create_table_queries = [session_item_create, user_session_create, song_user_create]
drop_table_queries = [session_item_drop, user_session_drop, song_user_drop]
