import pandas as pd

def execute_query(session, query):
    """Executes a query and returns the result

    Args:
        session (`cassandra.cluster.Session`): cassandra session object
        query (str): query to drop table

    Returns:
        result (`cassandra.cluster.ResultSet`): cassandra result set
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
        session (`cassandra.cluster.Session`): cassandra session object
        df (`pandas.core.frame.DataFrame`): dataframe containing values to insert
        columns (list): columns to insert
        query (str): query to drop table
    Returns:
        result (`cassandra.cluster.ResultSet`): cassandra result set
    """
    for v in df[columns].itertuples(index=False):
        session.execute(query, v)


def result_as_df(result_set, columns):
    """Coverts result set to a pandas data frame
    Args:
        result (`cassandra.cluster.ResultSet`): cassandra result set
        columns (list): column names for results
    Returns:
        df (`pandas.core.frame.DataFrame`): dataframe containing results
    """
    df = pd.DataFrame(list(result_set), columns=columns)

    return df
