import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.types import TimestampType
from pyspark.sql.functions import udf, col, monotonically_increasing_id
from pyspark.sql.functions import year, month, dayofmonth, dayofweek, hour, weekofyear, date_format


config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config.get('AWS', 'AWS_ACCESS_KEY_ID')
os.environ['AWS_SECRET_ACCESS_KEY']=config.get('AWS', 'AWS_SECRET_ACCESS_KEY')


def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """Processes song data file from S3 Bucket
    Args:
        spark(:obj:`pyspark.sql.session.SparkSession`): 
        input_data (str): S3 bucket where song files are stored
        output (str): S3 bucket file path to store resulting files

    Returns:
        None
    """
    # get filepath to song data file
    song_data = input_data+'song_data/*/*/*/*.json'
    
    # read song data file
    df = spark.read.json(song_data)
    df.createOrReplaceTempView("song_data_table")

    # extract columns to create songs table
    songs_table = df.select('song_id', 'title', 'artist_id', 'year', 'duration')
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.parquet(output_data + 'songs.parquet', partitionBy=('year', 'artist_id'), mode='overwrite')

    # extract columns to create artists table
    artists_table = df.selectExpr('artist_id AS artist_id', 'artist_name AS name', 
                                  'artist_location AS location', 'artist_latitude AS latitude', 
                                  'artist_longitude AS longitude')
    
    # write artists table to parquet files
    artists_table.write.parquet(output_data + 'artists.parquet', mode='overwrite')


def process_log_data(spark, input_data, output_data):
    """Processes song data file from S3 Bucket
    Args:
        spark(:obj:`pyspark.sql.session.SparkSession`): 
        input_data (str): S3 bucket where song files are stored
        output (str): S3 bucket file path to store resulting files

    Returns:
        None
    """
    # get filepath to log data file
    log_data = input_data + 'log_data/*/*/*.json'

    # read log data file
    df = spark.read.json(log_data)
    
    # filter by actions for song plays
    df = df.filter(df.page == 'NextSong')

    # extract columns for users table    
    users_table = df.selectExpr('userId AS user_id', 'firstName AS first_name', 
                                'lastName AS last_name', 'gender AS gender', 
                                'level AS level')
    
    # write users table to parquet files
    users_table.write.parquet(output_data + 'users.parquet', mode='overwrite')

    # create timestamp column from original timestamp column
    # get_timestamp = udf(lambda ms: datetime.fromtimestamp(ms // 1000), TimestampType())
    # df = df.withColumn('timestamp', get_timestamp(col('ts')))
    
    # create datetime column from original timestamp column
    get_timestamp = udf(lambda ms: datetime.fromtimestamp(ms // 1000), TimestampType())
    df = df.withColumn('datetime', get_timestamp(col('ts')))
    
    # extract columns to create time table
    time_table = df.selectExpr('datetime AS start_time', 'hour(datetime) AS hour', 
                               'dayofmonth(datetime) AS day', 'weekofyear(datetime) AS week', 
                               'month(datetime) AS month', 'year(datetime) AS year', 
                               'dayofweek(datetime) AS weekday')
    
    # write time table to parquet files partitioned by year and month
    time_table.write.parquet(output_data + 'time.parquet', partitionBy=('year', 'month'), mode='overwrite')

    # read in song data to use for songplays table
    song_df = spark.sql('select * from song_data_table')

    # extract columns from joined song and log datasets to create songplays table 
    cond = [df.song == song_df.title, df.artist == song_df.artist_name, df.length == song_df.duration]
    songplays_table = df.join(song_df, cond, 'inner') \
                        .selectExpr('datetime AS start_time', 'userID AS user_id',
                                    'month(datetime) AS month', 'year(datetime) AS year',
                                    'level AS level', 'song_id AS song_id', 
                                    'artist_id AS artist_id', 'sessionId AS session_id', 
                                    'location AS location', 'userAgent AS user_agent')
    songplays_table = songplays_table.withColumn('songplay_id', monotonically_increasing_id())

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.parquet(output_data + 'songplays.parquet', partitionBy=('year', 'month'), mode='overwrite')


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://udacity-dend/"
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
