import random
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd

# Define the start date of the DAG
start_date = datetime(year=2024, month=10, day=15)

# Define default arguments for the DAG
default_args = {
    'owner': 'saisunny',
    'depends_on_past': False,
    'backfill': False
}

# Set parameters for the task
num_rows = 50
output_file = './account_dim_large_data.csv'

# Variables to store data
account_ids = []
account_types = []
statuses = []
customer_ids = []
balances = []
opening_dates = []

# Function to generate random data
def generate_random_data(row_num):
    account_id = f'A{row_num:05d}'
    account_type = random.choice(['SAVINGS', 'CHECKING'])
    status = random.choice(['ACTIVE', 'INACTIVE'])
    customer_id = f'C{random.randint(1, 1000):05d}'
    balance = round(random.uniform(100.00, 10000.00), 2)

    now = datetime.now()
    random_date = now - timedelta(days=random.randint(0, 365))
    opening_date_millis = int(random_date.timestamp() * 1000)

    return account_id, account_type, status, customer_id, balance, opening_date_millis

# Function to generate the full dataset
def generate_account_dim_data():
    row_num = 1
    while row_num <= num_rows:
        account_id, account_type, status, customer_id, balance, opening_date_millis = generate_random_data(row_num)

        account_ids.append(account_id)
        account_types.append(account_type)
        statuses.append(status)
        customer_ids.append(customer_id)
        balances.append(balance)
        opening_dates.append(opening_date_millis)
        row_num += 1

    # Create a DataFrame to store the generated data
    df = pd.DataFrame({
        'account_id': account_ids,
        'account_type': account_types,
        'status': statuses,
        'customer_id': customer_ids,
        'balance': balances,
        'opening_date': opening_dates
    })

    # Output to CSV
    df.to_csv(output_file, index=False)
    print(f'CSV file {output_file} with {num_rows} rows has been generated successfully!')

# Define the DAG
with DAG(
    'account_dim_generator',
    default_args=default_args,
    description='DAG to generate random account data and output to CSV',
    schedule_interval=timedelta(days=1),
    start_date=start_date,
    tags=['schema'],
) as dag:

    # Define the start task
    start = EmptyOperator(task_id='start_task')

    # Define the Python task to generate the data
    generate_account_data_task = PythonOperator(
        task_id='generate_account_dim_data',
        python_callable=generate_account_dim_data
    )

    # Define the end task
    end = EmptyOperator(task_id='end_task')

    # Set up task dependencies
    start >> generate_account_data_task >> end