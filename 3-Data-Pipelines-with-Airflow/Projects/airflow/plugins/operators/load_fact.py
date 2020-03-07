from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):
    """Custom Operator for loading data into fact tables.
    
    Attributes:
        ui_color (str): color code for task in Airflow UI.
        insert_template (str): template string for inserting data.
        
    """
    ui_color = '#F98866'
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
        """Initializes a Fact Load Operator.
        Args:
            redshift_conn_id (str): Airflow connection ID for redshift database.
            query (str): Query used to populate fact table.
            target_table (str): Name of fact table.
            truncate (bool): Flag that determines if table is truncated before insert.

        """
        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.query = query
        self.target_table = target_table
        self.truncate = truncate

    def execute(self, context):
        """Executes task for loading a fact table.
        Args:
            context (:obj:`dict`): Dict with values to apply on content.
            
        """
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        if self.truncate:
            self.log.info(f'Truncating table: {self.target_table}')
            redshift.run(f'TRUNCATE TABLE {self.target_table}')
            
        insert_query = LoadFactOperator.insert_template.format(self.target_table, self.query)
        self.log.info(f'Loading Fact table: {self.target_table}')
        redshift.run(insert_query)
        self.log.info(f'Successfully Loaded Fact table: {self.target_table}')
