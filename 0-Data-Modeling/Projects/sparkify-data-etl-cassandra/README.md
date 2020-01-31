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

## Run Project

* Open Jupter notebook in directory
```bash
(venv) $ jupyter notebook
```