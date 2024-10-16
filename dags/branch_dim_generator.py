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
output_file = './branch_dim_large_data.csv'

# Variables to store data
cities = ["London", "Manchester", "Birminghan", "Glasgow", "Edinburgh"]
regions= ["London", "Greater Manchester", "West Midlands", "Scotland", "Finland"]
postcodes= ["EC1A 1BB", "M1 1AE", "B1 1AA", "G1 1AA", "EH1 1AA"]


# Function to generate random data
# Function to generate random branch data
def generate_random_data(row_num):
    branch_id = f"B{row_num:04d}"
    branch_name = f"Branch {row_num}"
    branch_address = f"{random.randint(a=1, b=999)} {random.choice(['High St', 'King St', 'Queen St', 'Church Rd', 'Church Street'])}"
    city = random.choice(cities)
    region = random.choice(regions)
    postcode = random.choice(postcodes)

    # Generate opening date in milliseconds
    now = datetime.now()
    random_date = now - timedelta(days=random.randint(a=0, b=3650))  # Random date within the last 10 years
    opening_date_millis = int(random_date.timestamp() * 1000)  # Convert to milliseconds since epoch

    return branch_id, branch_name, branch_address, city, region, postcode, opening_date_millis

# Initialize lists to store data

# Initialize lists to store data
branch_ids = []
branch_names = []
branch_addresses = []
cities_list = []
regions_list = []
postcodes_list = []
opening_dates = []

def generate_branch_dim_data():
    # Generate data using a while loop
    row_num = 1
    while row_num <= num_rows:
        data = generate_random_data(row_num)
        branch_ids.append(data[0])
        branch_names.append(data[1])
        branch_addresses.append(data[2])
        cities_list.append(data[3])
        regions_list.append(data[4])
        postcodes_list.append(data[5])
        opening_dates.append(data[6])
        row_num += 1

    # Create a DataFrame
    df = pd.DataFrame({
        "branch_id": branch_ids,
        "branch_name": branch_names,
        "branch_address": branch_addresses,
        "city": cities_list,
        "region": regions_list,
        "postcode": postcodes_list,
        "opening_date": opening_dates
    })

    # Save DataFrame to CSV
    df.to_csv(output_file, index=False)

    print(f"CSV file '{output_file}' with {num_rows} rows has been generated successfully.")

# Define the DAG
with DAG(
    'branch_dim_generator',
    default_args=default_args,
    description='DAG to generate random branch data and output to CSV',
    schedule_interval=timedelta(days=1),
    start_date=start_date,
    tags=['schema'],
) as dag:

    # Define the start task
    start = EmptyOperator(task_id='start_task')

    # Define the Python task to generate the data
    generate_branch_data_task = PythonOperator(
        task_id='generate_branch_dim_data',
        python_callable=generate_branch_dim_data
    )

    # Define the end task
    end = EmptyOperator(task_id='end_task')

    # Set up task dependencies
    start >> generate_branch_data_task >> end