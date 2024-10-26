import random
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd

from pinot_table_operator import PinotTableSubmitOperator

# Define the start date of the DAG
start_date = datetime(year=2024, month=10, day=16)

# Define default arguments for the DAG
default_args = {
    'owner': 'saisunny',
    'depends_on_past': False,
    'backfill': False
}

with DAG(
    dag_id='table_dag',
    default_args=default_args,
    description='To Submit All The Tables In A Folder To Apache Pinot',
    start_date=start_date,
    tags=['table'],
    schedule_interval=timedelta(days=1),
) as dag:

    start = EmptyOperator(task_id='start')

    submit_table = PinotTableSubmitOperator(
        task_id='submit_table',
        folder_path='/opt/airflow/dags/tables',
        pinot_url='http://pinot-controller:9000/tables'
    )

    end = EmptyOperator(task_id='end')

    start >> submit_table >> end


