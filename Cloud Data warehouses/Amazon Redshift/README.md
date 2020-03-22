# Implementing SQL Datawarehouse on AWS


### Introduction
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

### Project Scope
Using AWS cloud services, create Amazon Redshift cluster that serves as datawarehouse for Sparkify Application data.
Create required Schema, database, IAM role and database roles. 
Write the SQL queries to create and load the tables to refelct the start schema. 
Build the ETL pipeline (etl.py) using Python that extracts the information from JSON logs stored on S3 buckets and loads the data into Amazon Redshift. 

### Schema Design 

###### Staging Tables

staging_events -> Songs metadata loaded into staging tables. 
staging_songs -> Songs data will loaded in songs tables

###### Fact Table

songplays -> Records in log data associated with song plays

###### Dimension Tables

users -> User using the app

songs -> Songs from the Sparkify App

artists -> Song artists

time -> Songplay timestamps

### Steps Followed

1. Update the DWH CFG files. 

'''
[CLUSTER]
HOST=""
DB_NAME=sparkifydb
DB_USER=dwhadm
DB_PASSWORD=""
DB_PORT=5439

[IAM_ROLE]
ARN=

[S3]
LOG_DATA='s3://udacity-dend/log_data'
LOG_JSONPATH='s3://udacity-dend/log_json_path.json'
SONG_DATA='s3://udacity-dend/song_data'

[AWS]
KEY=
SECRET=

[DWH]
DWH_CLUSTER_TYPE       = multi-node
DWH_NUM_NODES          = 4
DWH_NODE_TYPE          = dc2.large
DWH_CLUSTER_IDENTIFIER = dwhCluster
DWH_DB                 = sparkifydb
DWH_DB_USER            = dwhadm
DWH_DB_PASSWORD        = ""
DWH_PORT               = 5439
DWH_IAM_ROLE_NAME      = ""
'''

2. Install the necessary python libraries, here we have used BOTO3 library to create Infrastructure as code.
3. Run the **create_cluster.py** to set up the amazon redshift cluster.
4. Update the **sql_queries.py** to load the data and create tables.
4. Run **create_tables.py** script to create the tables.
5. Run the **etl.py** to load the data from S3 to staging table and then to analytic tables. 
6. Test the loading process by querying tables using test.ipynb. 
7. Delete the cluster on aws.

### Files description: 

create_tables.py - Executes the sql_queries module to drop and creates fact and dimension tables as well Sparkify Database. 
Please run this script before every iteration to avoid data conflicts or duplication.

sql_queries.py - Contains the SQL statements to insert / select / drop and create tables.

etl.py - Loads the data from S3 into staging tables, executes sql_queries.py to load the data from staging tables to analytics tables

test.ipynb - The queries to verify the data loaded in the database.

README.md - Project description

### References

https://classroom.udacity.com/nanodegrees/nd027/parts/69a25b76-3ebd-4b72-b7cb-03d82da12844/modules/58ff61b9-a54f-496d-b4c7-fa22750f6c76/lessons/b3ce1791-9545-4187-b1fc-1e29cc81f2b0/concepts/32c31df5-7a94-49b4-90da-53308ac2edd5