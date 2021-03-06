# Sparkify's Data Pipeline with Airflow
##### Table of Contents  
- [Introduction](#introduction)
- [Set Up](#setup)
- [Usage](#usage)

## Introduction
Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. Projects sets up a data Pipeline to do the following:
* Stage songs and events data from S3 to Redshift
* Perform transformations to create star schema
* Run data quality checks

### Datasets
* **Song Dataset**:
    The first dataset is a subset of real data from the [Million Song Dataset](https://labrosa.ee.columbia.edu/millionsong). Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset.

    ```
    song_data/A/B/C/TRABCEI128F424C983.json
    song_data/A/A/B/TRAABJL12903CDCF1A.json
    ```
    And below is an example of what a single song file, `TRAABJL12903CDCF1A.json`, looks like.
    ```
    {"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
    ```
* **Log Dataset**:
    The second dataset consists of log files in JSON format generated by this event simulator based on the songs in the dataset above. These simulate app activity logs from a music streaming app based on specified configurations.

    The log files in the dataset are partitioned by year and month. For example, here are filepaths to two files in this dataset.

    ```
    log_data/2018/11/2018-11-12-events.json
    log_data/2018/11/2018-11-13-events.json
    ```
    And below is an example of what the data in a log file, `2018-11-12-events.json`, looks like.
    <img src="../README_IMGS/log_data_sample.png"/>

### Data Schema
#### Fact Table
* **songplays** - records in log data associated with song plays i.e. records with page `NextSong`
    * `songplay_id`, `start_time`, `user_id`, `level`, `song_id`, `artist_id`, `session_id`, `location`, `user_agent`

#### Dimension Tables
* **users** - users in the app
    * `user_id`, `first_name`, `last_name`, `gender`, `level`
* **songs** - songs in music database
    * `song_id`, `title`, `artist_id`, `year`, `duration`
* **artists** - artists in music database
    * `artist_id`, `name`, `location`, `lattitude`, `longitude`
* **time** - timestamps of records in <b>songplays</b> broken down into specific units
    * `start_time`, `hour`, `day`, `week`, `month`, `year`, `weekday`

###### <u>entity relationship diagram showing data schema</u>
<img src="../README_IMGS/Sparkify ERD.png"/>
    
###### <u>data pipeline graph in airflow UI</u>
<img src="../README_IMGS/airflow_data_pipeline.png"/>



## Set Up
1. Python3 is required
2. Install `pip3`
3. Create virtual env, Set Up Apache Airflow & install dependencies:
```bash
$ python -m venv venv
$ source venv/bin/activate
(venv) $ export AIRFLOW_HOME=$(pwd)
(venv) $ pip install -r requirements.txt
(venv) $ airflow initdb
```
4. Run Webserver
```bash
(venv) $ export AIRFLOW_HOME=$(pwd)
(venv) $ airflow webserver -p 8080
```
5. Run Scheduler
```bash
(venv) $ export AIRFLOW_HOME=$(pwd)
(venv) $ airflow scheduler
```

## Usage
1. create aws config
   * create file `dwh.cfg`
   * add the following contents (fill the fields)
    ```bash
    [CLUSTER]
    HOST=
    DB_NAME=
    DB_USER=
    DB_PASSWORD=
    DB_PORT=
   ```
2. create redshift tables for pipeline
   ```bash
   (venv) $ python create_tables.py
   ```
1. Visit `localhost:8080`
2. Run the dag `sparkify_etl_dag.py`