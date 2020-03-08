# sparkify-pipeline
Build a Workflow Pipeline to do the following
* Stage songs and events data from S3 to Redshift
* Perform transformations to create star schema
* Run data quality checks

## Set Up
1. Python3 is required
2. Install `pip3`
3. Create virtual env, Set Up Apache Airflow & install dependencies:
```bash
$ python -m venv venv
$ source venv/bin/activate
(venv) $ export AIRFLOW_HOME=$(pwd)
(venv) $ pip install apache-airflow
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
1. Visit `localhost:8080`