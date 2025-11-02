import os
import sys
from datetime import datetime, timedelta
from airflow import DAG

from airflow.providers.standard.operators.python import PythonOperator
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipelines.aws_s3_pipeline import upload_s3_pipeline
from pipelines.x_pipeline import x_pipeline

default_args = {
    'owner': 'Anass Seghir',
    'start_date': datetime(2023, 10, 22),
    'retries': 1
}

file_postfix = datetime.now().strftime("%Y%m%d")

dag = DAG(
    dag_id='etl_x_pipeline',
    default_args=default_args,
    schedule='@daily',
    catchup=False,
    tags=['x', 'etl', 'pipeline']
)

# extraction from x
extract = PythonOperator(
    task_id='x_extraction',
    python_callable=x_pipeline,
    op_kwargs={
        'file_name': f'x_{file_postfix}.csv'
    },
    execution_timeout=timedelta(minutes=10),
    dag=dag
)

# upload to s3
upload_s3 = PythonOperator(
    task_id='s3_upload',
    python_callable=upload_s3_pipeline,
    dag=dag
)

extract >> upload_s3