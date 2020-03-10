import pandas as pd
from cassandra.cluster import Cluster


def create_cluster_keyspace():
    """Create Cluster and KeySpace, Sets KeySpace
    Args:
        None
    Returns: 
        cluster (:obj:`cassandra.cluster`): cassandra cluster object
        session (:obj:`cassandra.cluster.Session`): cassandra session object
    """
    # This should make a connection to a Cassandra instance your local machine
    try: 
        cluster = Cluster(['127.0.0.1'])
        # To establish connection and begin executing queries, need a session
        session = cluster.connect()   
    except Exception as e:
        print(e)

    # Create Keyspace
    try:
        session.execute("""
        CREATE KEYSPACE IF NOT EXISTS sparkifydb
        WITH REPLICATION = 
        { 'class': 'SimpleStrategy', 'replication_factor': 1 }
        """)
    except Exception as e:
        print(e)

    # Set Keyspace
    try:
        session.set_keyspace('sparkifydb')
    except Exception as e:
        print(e)

    return cluster, session


def execute_query(session, query):
    """Executes a query and returns the result

    Args:
        session (:obj:`cassandra.cluster.Session`): cassandra session object
        query (str): query to drop table
    Returns:
        result (:obj:`cassandra.cluster.ResultSet`): cassandra result set
    """
    result = None

    try:
        result = session.execute(query) 
    except Exception as e:
        print(e)

    return result


def insert_from_df(session, df, columns, query):
    """Executes a query and returns the result

    Args:
        session (:obj:`cassandra.cluster.Session`): cassandra session object
        df (:obj:`pandas.core.frame.DataFrame`): dataframe containing values to insert
        columns (:obj: list of str): columns to insert
        query (str): query to drop table
    Returns:
        result (:obj:`cassandra.cluster.ResultSet`): cassandra result set
    """
    for v in df[columns].itertuples(index=False):
        session.execute(query, v)


def result_as_df(result_set, columns):
    """Coverts result set to a pandas data frame
    Args:
        result (:obj:`cassandra.cluster.ResultSet`): cassandra result set
        columns (list): column names for results
    Returns:
        df (:obj:`pandas.core.frame.DataFrame`): dataframe containing results
    """
    df = pd.DataFrame(list(result_set), columns=columns)

    return df
