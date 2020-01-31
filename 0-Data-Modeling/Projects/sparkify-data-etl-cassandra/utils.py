

def execute_query(session, query):
    """Executes a query and returns the result

    Args:
        session (`cassandra.cluster.Session`): cassandra session object
        query (str): query to drop table

    Returns:
        result (`cassandra.cluster.ResultSet`): cassandra result set
    """
    try:
        result = session.execute(query) 
    except Exception as e:
        print(e)

    return result


def insert_from_csv(session, query, l):
    """Executes a query and returns the result

    Args:
        session (`cassandra.cluster.Session`): cassandra session object
        query (str): query to drop table
        l (tuple): column indexes to insert
    Returns:
        result (`cassandra.cluster.ResultSet`): cassandra result set
    """
