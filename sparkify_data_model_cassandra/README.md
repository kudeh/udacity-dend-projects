# Sparkify's Data Modeling With Apache Cassandra

##### Table of Contents  
- [Introduction](#introduction)
- [Set Up](#setup)
- [Usage](#usage)

## Introduction
* Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app.
* Project sets up an ETL workflow that creates the data models in an apache cassandra database.

### Datasets
This project uses one dataset `event_data`. The directory of CSV files partitioned by date. Here are examples of filepaths to two files in the dataset:
```
event_data/2018-11-08-events.csv
event_data/2018-11-09-events.csv
```

### Project Structure
Files and their purposes: 

| file | description |
| --- | --- |
| `sql_queries.py` | contains all queries used in project |
| `utils.py` | contains all utility functions used in project |
| `etl.py` | contains function for preprocessing event data files |
| `main.ipynb` | entry point to execute project |
| `Project_1B_ Project_Template.ipynb` | monolith: does everything the above files do in one notebook |

## Setup

1. Python3 is required
2. Install `pip3`
3. Setup Apache Cassandra:
    * Install [Cassandra](http://cassandra.apache.org/download/)
    * Start Apache Cassandra
    ```bash
    $ brew services start cassandra
    ```
5. Create virtual env, install dependencies:
```bash
$ python -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ ipython kernel install --user --name=projectname  
```

## Usage
* Open Jupter notebook in directory
    ```bash
    (venv) $ jupyter notebook
    ```
* Run Notebook: `main.ipynb`