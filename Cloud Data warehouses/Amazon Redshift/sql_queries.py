import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

IAM_ROLE = config['IAM_ROLE']['ARN']
LOG_DATA = config['S3']['LOG_DATA']
SONG_DATA = config['S3']['SONG_DATA']
LOG_JSONPATH = config['S3']['LOG_JSONPATH']

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_events
(artist TEXT,
auth TEXT,
first_name TEXT,
gender CHAR(1),
item_session INTEGER,
last_name TEXT,
length NUMERIC,
level TEXT,
location TEXT,
method TEXT,
page TEXT,
registration NUMERIC,
session_id INTEGER,
song TEXT,
status INTEGER,
ts BIGINT,
user_agent TEXT,
user_id INTEGER )""")

staging_songs_table_create = ("""
CREATE  TABLE IF NOT EXISTS staging_songs
(num_songs INTEGER,
artist_id TEXT,
artist_latitude NUMERIC,
artist_longitude NUMERIC,
artist_location TEXT,
artist_name TEXT,
song_id TEXT,
title TEXT,
duration NUMERIC,
year INTEGER)""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays 
(songplay_id INT IDENTITY(1,1) PRIMARY KEY, 
 start_time TIMESTAMP SORTKEY DISTKEY, 
 user_id INT NOT NULL, 
 level TEXT, 
 song_id TEXT, 
 artist_id TEXT, 
 session_id INT, 
 location TEXT, 
 user_agent TEXT);
 """)

user_table_create = (""" 
CREATE TABLE IF NOT EXISTS users 
(user_id INT SORTKEY PRIMARY KEY, 
first_name TEXT NOT NULL, 
last_name TEXT NOT NULL, 
gender CHAR(1), 
level TEXT);
""")

song_table_create = (""" 
CREATE TABLE IF NOT EXISTS songs 
(song_id TEXT SORTKEY PRIMARY KEY, 
title TEXT, 
artist_id TEXT, 
year INT, 
duration FLOAT(5));
""")

artist_table_create = (""" 
CREATE TABLE IF NOT EXISTS artists 
(artist_id TEXT SORTKEY PRIMARY KEY, 
name TEXT, 
location TEXT, 
latitude FLOAT(5), 
longitude FLOAT(5) );
""")

time_table_create = (""" 
CREATE TABLE IF NOT EXISTS time 
(start_time TIMESTAMP DISTKEY SORTKEY PRIMARY KEY, 
hour INT, 
day INT, 
week INT, 
month INT, 
year INT, 
weekday INT);
""")

# STAGING TABLES

staging_events_copy = ("""
COPY staging_events from {}
iam_role {}
json {}
""").format(LOG_DATA,IAM_ROLE,LOG_JSONPATH)

staging_songs_copy = (""" COPY staging_songs from {}
iam_role {}
json 'auto'
""").format(SONG_DATA,IAM_ROLE)

# FINAL TABLES

songplay_table_insert = ("""INSERT INTO songplays 
(start_time, user_id, level, song_id, artist_id, session_id,location, user_agent)
SELECT  timestamp 'epoch' + se.ts/1000 * interval '1 second' as start_time, 
se.user_id, se.level, ss.song_id, ss.artist_id, se.session_id, se.location, se.user_agent
FROM staging_events se, staging_songs ss
WHERE se.page = 'NextSong' AND
se.song = ss.title AND
se.artist = ss.artist_name AND
se.length = ss.duration
""")

user_table_insert = ("""INSERT INTO users 
(user_id,first_name,last_name,gender,level) 
SELECT  distinct user_id, 
first_name,
last_name, 
gender,level
from staging_events where page = 'NextSong'
""")

song_table_insert = ("""INSERT INTO songs
(song_id, title, artist_id, year, duration)
SELECT song_id, 
title, 
artist_id, 
year, 
duration
FROM staging_songs
WHERE song_id IS NOT NULL
""")

artist_table_insert = ("""INSERT INTO artists
(artist_id, name, location, latitude, longitude)
SELECT distinct artist_id, 
artist_name, 
artist_location, 
artist_latitude, 
artist_longitude 
FROM staging_songs
WHERE artist_id IS NOT NULL
""")

time_table_insert = ("""INSERT INTO time
(start_time, hour, day, week, month, year, weekDay)
SELECT start_time, extract(hour from start_time), 
extract(day FROM start_time),
extract(week FROM start_time), 
extract(month FROM start_time),
extract(year FROM start_time), 
extract(dayofweek FROM start_time)
FROM songplays
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
