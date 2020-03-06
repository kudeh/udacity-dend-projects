from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'
    insert_template = """
        INSERT INTO {} ({})
        {};
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentials_id="",
                 query="",
                 target_table="",
                 target_columns=[],
                 truncate=False,
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.query = query
        self.target_table = target_table
        self.target_columns = ', '.join(target_columns)
        self.truncate = truncate
        

    def execute(self, context):
        
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info('Running LoadFactOperator for {} table'.format(self.target_table))
        
        if self.truncate:
            redshift.run('DELETE FROM {}'.format(self.target_table))
            
        insert_query = insert_template.format(self.target_table, self.target_columns, self.query)
        redshift.run(insert_query)
