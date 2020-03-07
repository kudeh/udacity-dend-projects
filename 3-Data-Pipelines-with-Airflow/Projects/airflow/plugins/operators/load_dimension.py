from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):
    """Custom Operator for loading data into dimension tables.
    
    Attributes:
        ui_color (str): color code for task in Airflow UI.
        insert_template (str): template string for inserting data.
        
    """
    ui_color = '#80BD9E'
    insert_template = """
        INSERT INTO {} ({});
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 query="",
                 target_table="",
                 truncate=False,
                 *args, **kwargs):
        """Initializes a Dimension Load Operator.
        Args:
            redshift_conn_id (str): Airflow connection ID for redshift database.
            query (str): Query used to populate dimension table.
            target_table (str): Name of dimension table.
            truncate (bool): Flag that determines if table is truncated before insert.

        """
        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.query = query
        self.target_table = target_table
        self.truncate = truncate

    def execute(self, context):
        """Executes task for loading a dimension table.
        Args:
            context (:obj:`dict`): Dict with values to apply on content.
            
        """
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        if self.truncate:
            self.log.info(f'Truncating table: {self.target_table}')
            redshift.run(f'TRUNCATE TABLE {self.target_table}')
            
        insert_query = LoadDimensionOperator.insert_template.format(self.target_table, self.query)
        self.log.info(f'Loading Dimension table: {self.target_table}')
        redshift.run(insert_query)
        self.log.info(f'Successfully Loaded Dimension table: {self.target_table}')
