# sparkify-dwh

## Installation & Setup

1. Python3 is required
2. Install `pip3`
3. create aws/boto3 config
   * create file `dwh.cfg`
   * add the following contents (fill the aws key and secret)
    ```bash
    [AWS]
    KEY=[enter aws key here]
    SECRET=[enter aws secret here]

    [DWH] 
    DWH_CLUSTER_TYPE=multi-node
    DWH_NUM_NODES=4
    DWH_NODE_TYPE=dc2.large

    DWH_IAM_ROLE_NAME=dwhRole
    DWH_CLUSTER_IDENTIFIER=dwhCluster
    DWH_DB=dwh
    DWH_DB_USER=dwhuser
    DWH_DB_PASSWORD=Passw0rd
    DWH_PORT=5439
    ```
4. Create virtual env, install dependencies:
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