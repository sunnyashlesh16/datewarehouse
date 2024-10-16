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

# Parameters for the task
num_rows = 100  # Number of rows to generate
output_file = './customer_dim_large_data.csv'  # Output file name

# Variables to store data
customer_ids = []
first_names = []
last_names = []
emails = []
phone_numbers = []
registration_dates = []

# Function to generate random customer data
def generate_random_data(row_num):
    customer_id = f'C{row_num:05d}'
    first_name = f"FirstName{row_num}"
    last_name = f"LastName{row_num}"
    email = f"customer{row_num}@example.com"
    phone_number = f"+1-800-{random.randint(1000000, 9999999)}"

    # Generate timestamp with milliseconds
    now = datetime.now()
    random_date = now - timedelta(days=random.randint(0, 3650))  # Random date within the last 10 years
    registration_date_millis = int(random_date.timestamp() * 1000)  # Convert to milliseconds

    return customer_id, first_name, last_name, email, phone_number, registration_date_millis

# Function to generate the full dataset
def generate_customer_dim_data():
    row_num = 1
    while row_num <= num_rows:
        customer_id, first_name, last_name, email, phone_number, registration_date_millis = generate_random_data(row_num)

        customer_ids.append(customer_id)
        first_names.append(first_name)
        last_names.append(last_name)
        emails.append(email)
        phone_numbers.append(phone_number)
        registration_dates.append(registration_date_millis)

        row_num += 1

    # Create a DataFrame to store the generated data
    df = pd.DataFrame({
        'customer_id': customer_ids,
        'first_name': first_names,
        'last_name': last_names,
        'email': emails,
        'phone_number': phone_numbers,
        'registration_date': registration_dates
    })

    # Output to CSV
    df.to_csv(output_file, index=False)
    print(f'CSV file {output_file} with {num_rows} rows has been generated successfully!')

# Define the DAG
with DAG(
    'customer_dim_generator',
    default_args=default_args,
    description='DAG to generate random customer data and output to CSV',
    schedule_interval='@daily',
    start_date=start_date,
    tags=['dimension'],
) as dag:

    # Define the start task
    start = EmptyOperator(task_id='start_task')

    # Define the Python task to generate the data
    generate_customer_data_task = PythonOperator(
        task_id='generate_customer_dim_data',
        python_callable=generate_customer_dim_data
    )

    # Define the end task
    end = EmptyOperator(task_id='end')

    # Set up task dependencies
    start >> generate_customer_data_task >> end