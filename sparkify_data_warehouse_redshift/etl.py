import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """Copies data from S3 bucket and stages in redshift.
    Args:
        cur (:obj:`psycopg2.extensions.cursor`): Cursor for connection
        con (:obj:`psycopg2.extensions.connection`): database connection
    Returns:
        None
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """Inserts data into redshift db tables.
    Args:
        cur (:obj:`psycopg2.extensions.cursor`): Cursor for connection
        con (:obj:`psycopg2.extensions.connection`): database connection
    Returns:
        None
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()