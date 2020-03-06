from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 query="",
                 target_table="",
                 truncate=True,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.query = query
        self.target_table = target_table
        self.truncate = truncate
        """
        """

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        if self.truncate:
            self.log.info(f'Truncating table: {self.target_table}')
            redshift.run(f'TRUNCATE TABLE {self.target_table}')
            
        insert_query = LoadDimensionOperator.insert_template.format(self.target_table, self.query)
        self.log.info(f'Loading Dimension table: {self.target_table}')
        redshift.run(insert_query)
        self.log.info(f'Successfully Loaded Dimension table: {self.target_table}')
