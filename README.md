# Data Engineer Nanodegree Projects
My Project Solutions From [Udacity Data Engineer Nanodegree Program](https://www.udacity.com/course/data-engineer-nanodegree--nd027).

## 1. [Data Modeling with PostgreSQL](https://github.com/kudeh/udacity-dend-projects/tree/master/sparkify_data_model_postgres)
Set up a relational database using PostgreSQL to model user activity data for sparkify - a music streaming app.

* **Tasks Completed:**
    * Administrated a PostgreSQL DB locally.
    * Developed create a star schema optimized for queries on the fact & dimension tables
    * Implemented ETL pipeline to create and load data into fact and dimension tables.

* **Concepts Learned:**
    * Normalization
    * ACID Principle
    * Star & Snowflake Schema
    * ETL Workflows

* **Core Technologies Used:**
    * Python (Pandas, Jupyter, psycopg2)
    * PosgreSQL

## 2. [NoSQL Data Modeling with Apache Cassandra](https://github.com/kudeh/udacity-dend-projects/tree/master/sparkify_data_model_cassandra)
Set up noSQL database tables using Apache Cassandra to answer business questions about user activity for sparkify - a music streaming app.

* **Tasks Completed:**
    * Administrated a Apache Cassandra DB locally
    * Created Tables in Keyspace based on defined queries that denormalizes the star schema, optimized to answer business questions
    * Implemented ETL pipeline to create and load data into tables

* **Concepts Learned:**
    * Distribute Database Design
    * CAP(Consistency, Availability, Partition Tolerance) Theorem
    * Partitioning with Primary Key & Clustering Columns

* **Core Technologies Used:**
    * Python (Pandas, Jupyter, cassandra)
    * Apache Cassandra

## 3. [Data Warehousing with Amazon Redshift](https://github.com/kudeh/udacity-dend-projects/tree/master/sparkify_data_warehouse_redshift)
Set up a data warehouse using Amazon Redshift containing user activity data for sparkify - a music streaming app.

* **Tasks Completed:**
    * Administered a Redshift Cluster on AWS(Created roles & users)
    * Staged raw data from S3 into Redshift
    * Performed ETL to extract from staging tables, transform and create optimized tables for performing analytics

* **Concepts Learned:**
    * IAM Roles
    * COPY from S3
    * Distributed Columnar Database Design (DISTKEY, SORTKEY)

* **Core Technologies Used:**
    * Python (Pandas, Jupyter, psycopg2, boto3)
    * Apache Cassandra

## 4. [Data Lake with Apache Spark](https://github.com/kudeh/udacity-dend-projects/tree/master/sparkify_data_lake_spark)
Set up a spark data lake using Amazon EMR that performs analytics on user activity data for sparkify - a music streaming app.

* **Tasks Completed:**
    * Administered a EMR Cluster on AWS(Created roles & users)
    * Performed ETL to Read Data From S3 using PySpark, performs transformation and saves results as parquet files on S3

* **Concepts Learned:**
    * Schema On Read
    * Data Lake Implementation Options on AWS
    * Parquet Files

* **Core Technologies Used:**
    * Python (Pandas, PySpark)
    * Apache Spark
    * Amazon Elastic MapReduce(EMR)

## 5. [Data Pipelines with Apache Airflow](https://github.com/kudeh/udacity-dend-projects/tree/master/sparkify_data_pipeline_airflow)
Set up a data pipeline using Apache Airflow that schedules and monitors workflow for performing analytics on user activity data for sparkify - a music streaming app.

* **Tasks Completed:**
    * Administered a Apache Airflow (Setup connections, Server, UI, Scheduler)
    * Administered Amazon Redshift Database
    * Created Custom Operators For Performing Tasks to stage raw data to Redshift, load fact & dimension tables to redshift and perform quality checks on resulting data

* **Concepts Learned:**
    * Directed Acyclic Graphs(DAGs) relevance to data pipelines
    * Operators, Tasks, Hooks, Connections, Context Templating on Apache Airflow
    * Data Lineage, Scheduling, Backfilling, Partitioning and Quality Checks

* **Core Technologies Used:**
    * Python (airflow)
    * Apache Airflow


## 5. [Capstone Project](https://github.com/kudeh/udacity-dend-capstone)
For my capstone project I developed a data pipeline that creates an analytics database for querying information about immigration into the U.S on a monthly basis. The analytics tables are hosted in a Redshift Database and the pipeline implementation was done using Apache Airflow.