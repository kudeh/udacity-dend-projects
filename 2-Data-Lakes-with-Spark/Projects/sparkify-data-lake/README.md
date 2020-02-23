# sparkify-data-lake
* Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app.
* Project creates analytics model using song and log files in S3 Bucket using Spark on an EMR Cluster and writes the result to S3.

## Installation & Setup
1. Create Key-Pair on EC2
2. Create EMR Cluster
3. SSH to EMR Cluster


## Usage
* Submit `etl.py` as a spark job
   ```bash
   $ which spark-submit
   $ /usr/bin/spark-submit --master yarn ./etl.py
   ```