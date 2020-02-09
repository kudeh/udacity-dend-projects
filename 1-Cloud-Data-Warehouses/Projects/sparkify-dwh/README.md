# sparkify-dwh

## Installation & Setup

1. Python3 is required
2. Install `pip3`
3. Create Redshift DB AND ARN
   
4. create aws config
   * create file `dwh.cfg`
   * add the following contents (fill the aws key and secret)
    ```bash
    [CLUSTER]
    HOST=
    DB_NAME=
    DB_USER=
    DB_PASSWORD=
    DB_PORT=

    [IAM_ROLE]
    ARN=''

    [S3]
    LOG_DATA='s3://udacity-dend/log_data'
    LOG_JSONPATH='s3://udacity-dend/log_json_path.json'
    SONG_DATA='s3://udacity-dend/song_data'
    ```
5. Create virtual env, install dependencies:
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