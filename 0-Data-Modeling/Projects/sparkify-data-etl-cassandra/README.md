# sparkify-data-etl-cassandra

## Installation & Setup

1. Python3 is required
2. Install `pip3`
3. Setup Apache Cassandra:
    * Install [Cassandra](http://cassandra.apache.org/download/)
    * Start Apache Cassandra
    ```bash
    brew services start cassandra
    ```
5. Create virtual env, install dependencies:
```bash
$ python -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ ipython kernel install --user --name=projectname  
```

## Project Structure
Files and their purposes: 

| file | description |
| --- | --- |
| `sql_queries.py` | contains all queries used in project |
| `utils.py` | contains all utility functions used in project |
| `etl.py` | contains function for preprocessing event data files |
| `main.ipynb` | entry point to execute project |

## Run Project
* Open Jupter notebook in directory
```bash
(venv) $ jupyter notebook
```
* Run `main.ipynb`