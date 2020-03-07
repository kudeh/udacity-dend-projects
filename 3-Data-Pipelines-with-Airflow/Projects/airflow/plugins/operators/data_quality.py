from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):
    """Custom Operator for performing data quality check on a table.
    
    Attributes:
        ui_color (str): color code for task in Airflow UI.
        count_template (str): template string for checking if table contains data.
        
    """
    ui_color = '#89DA59'
    count_template = """
                     SELECT COUNT(*) 
                     FROM {}"""

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 query="",
                 result="",
                 *args, **kwargs):
        """Initializes a Data Quality Check Operator.
        Args:
            redshift_conn_id (str): Airflow connection ID for redshift database.
            table (str): Name of table to quality check.
            query (:obj:`str`, optional): Query use for testing table quality.
            result (:obj:`str`, optional): Expected result

        """
        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.query = query
        self.result = result

    def execute(self, context):
        """Executes task for data quality check.
        Args:
            context (:obj:`dict`): Dict with values to apply on content.
            
        """
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        self.log.info(f'Fetching Record count from {self.table}...')
        records = redshift.get_records(DataQualityOperator.count_template.format(self.table))
        
        self.log.info(f'Checking if {self.table} table contains returned results...')
        if len(records) < 1 or len(records[0]) < 1:
            raise ValueError(f'Fail: No results for {self.table} table')
            
        self.log.info(f'Checking if {self.table} table has records...')
        num_records = records[0][0]
        if num_records < 1:
            raise ValueError(f'Fail: 0 rows in {self.table} table')
        self.log.info(f'Has {records[0][0]} Records!')
        
        if self.result:
            self.log.info(f'Checking if {self.query} returns expected results')
            test_result = redshift.get_records(self.query)  
            
            if len(test_result) < 1 or len(test_result[0]) < 1:
                raise ValueError(f'Fail: No results for query: {self.query}')

            if test_result[0][0] != self.result:
                raise ValueError(f'Fail: Unexpected result, \nexpected: {self.result} \ngot: {test_result[0][0]}')
       
        self.log.info(f'Data Quality Check on {self.table} table was successful!')