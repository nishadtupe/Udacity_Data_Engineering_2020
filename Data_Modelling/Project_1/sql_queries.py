# DROP TABLES

songplay_table_drop = "drop table if exists songplays"
user_table_drop = "drop table if exists users"
song_table_drop = "drop table if exists songs"
artist_table_drop = "drop table if exists artists"
time_table_drop = "drop table if exists time"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays (songplay_id INT PRIMARY KEY, start_time TIMESTAMP, user_id INT, level VARCHAR(10)
, song_id VARCHAR(20), artist_id VARCHAR(20), session_id INT, location VARCHAR(60), user_agent VARCHAR(150));""")

user_table_create = (""" CREATE TABLE IF NOT EXISTS users (user_id INT PRIMARY KEY, first_name VARCHAR(30), last_name VARCHAR(30), gender CHAR(1), level VARCHAR(10));""")

song_table_create = (""" CREATE TABLE IF NOT EXISTS songs (song_id VARCHAR(20), title VARCHAR(100), artist_id VARCHAR(20), year INT, duration FLOAT(5));""")

artist_table_create = (""" CREATE TABLE IF NOT EXISTS artists (artist_id VARCHAR(20), name VARCHAR(100), location VARCHAR(100), latitude FLOAT(5), longitude FLOAT(5) );""")

time_table_create = (""" CREATE TABLE IF NOT EXISTS time (start_time TIMESTAMP, hour INT, day INT, week INT, month INT, year INT, weekday INT);""")

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplays (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT(songplay_id) DO NOTHING; """)

user_table_insert = ("""INSERT INTO users (user_id,first_name,last_name,gender,level) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""")

song_table_insert = (""" INSERT INTO songs (song_id, title, artist_id, year, duration) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;""")

artist_table_insert = (""" INSERT INTO artists (artist_id , name , location , latitude, longitude) VALUES (%s, %s, %s, %s, %s) ON  CONFLICT DO NOTHING ;""")


time_table_insert = (""" INSERT INTO time (start_time, hour, day, week, month, year, weekday)
VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING; """)

# FIND SONGS

song_select = (""" SELECT s.song_id, s.artist_id FROM songs s
JOIN artists ar on s.artist_id = ar.artist_id
WHERE s.title = %s
AND ar.name = %s
AND s.duration = %s
; """)

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]