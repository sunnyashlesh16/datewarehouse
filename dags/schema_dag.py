import random
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd

from pinot_schema_operator import PinotSchemaSubmitOperator

# Define the start date of the DAG
start_date = datetime(year=2024, month=10, day=16)

# Define default arguments for the DAG
default_args = {
    'owner': 'saisunny',
    'depends_on_past': False,
    'backfill': False
}

with DAG(
    dag_id='schema_dag',
    default_args=default_args,
    description='To Submit All The Schemas In A Folder To Apache Pinot',
    start_date=start_date,
    tags=['schema'],
    schedule_interval=timedelta(days=1),
) as dag:

    start = EmptyOperator(task_id='start')

    submit_schema = PinotSchemaSubmitOperator(
        task_id='submit_schema',
        folder_path='/opt/airflow/dags/schemas',
        pinot_url='http://pinot-controller:9000/schemas'
    )

    end = EmptyOperator(task_id='end')

    start >> submit_schema >> end


