# sparkify-data-etl
* Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app.
* Project creates data model with postgres and sets up ETL pipeline.


## Installation & Setup
1. Python 3 Required
2. Install `pip3`
3. 
    * Install [Postgres](https://www.postgresql.org/download/)
    * Create user `student`
    ```bash
    >> createuser --interactive --pwprompt
       Enter name of role to add: student
       Enter password for new role: student
       Enter it again: student
       Shall the new role be a superuser? (y/n) y
    >> createdb studentdb
    ```
4. Create virtual environment and install dependencies
    ```bash
    >> python3 -m venv venv
    >> source venv/bin/activate
    >> pip3 install -r requirements.txt
    ```

## Usage
1. Create Tables
    ```bash
    >> python create_tables.py
    ```
2. Run etl
    ```bash
    >> python etl.py
    ```
