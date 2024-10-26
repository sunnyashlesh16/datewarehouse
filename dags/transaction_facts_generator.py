from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
import sys
sys.path.append('/opt/airflow/plugins')
from kafka_operator import KafkaProduceOperator


start_date = datetime(2024, 10, 19)
default_args = {
    'owner': 'saisunny',
    'depends_on_past': False,
    'backfill': False
}

with DAG(
    dag_id='transaction_facts_generator',
    default_args=default_args,
    start_date=start_date,
    description='Transaction Facts Generator In To Kafka',
    schedule_interval=timedelta(days=1),
    tags=['fact_data'],
) as dag:
    start = EmptyOperator(
        task_id='start_task',
    )

    generate_txn_data = KafkaProduceOperator(
        task_id='generate_txn_fact_data',
        kafka_broker='kafka_broker:9092',
        kafka_topic='transaction_facts',
        num_records=100
    )

    end = EmptyOperator(
        task_id='end_task',
    )

    start >> generate_txn_data >> end
