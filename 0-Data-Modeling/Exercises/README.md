# Data Modeling Exercises

## Installation & Setup

1. Python3 is required
2. Install `pip3`
3. Setup Postgres:  
    * Install [Postgres](https://www.postgresql.org/download/)
    * Start Postgres
    ```bash
    $ pg_ctl -D /usr/local/var/postgres start
    ```
    * Create user `student`
    ```bash
    $ createuser --interactive --pwprompt
       Enter name of role to add: student
       Enter password for new role: student
       Enter it again: student
       Shall the new role be a superuser? (y/n) y
    $ createdb studentdb
    ```
* Create virtual env, install dependencies:
```bash
$ python -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ ipython kernel install --user --name=projectname  
```

## Run Exercises

* Open Jupter notebook in directory
```bash
(venv) $ jupyter notebook
```