import glob
from typing import Any

import requests
from airflow.models import BaseOperator
from airflow.utils.context import Context
from airflow.utils.decorators import apply_defaults


class PinotTableSubmitOperator(BaseOperator):

    @apply_defaults
    def __init__(self, folder_path, pinot_url, *args, **kwargs):
        super(PinotTableSubmitOperator, self).__init__(*args, **kwargs)
        self.folder_path = folder_path
        self.pinot_url = pinot_url

    def execute(self, context: Context) -> Any:
        try:
            table_files = glob.glob(self.folder_path + '/*.json')
            for table_file in table_files:
                with open(table_file, 'r') as file:
                    table_data = file.read()

                    #define the headers and submit the post request to pinot
                    headers = {'Content-Type': 'application/json'}
                    response = requests.post(self.pinot_url, data=table_data, headers=headers)

                    if response.status_code == 200:
                        self.log.info(f'{table_file} Table Successfully Submitted To Apache Pinot!')
                    else:
                        self.log.error(f'{table_file} Table Submission Failed To Submit With {response.status_code} - {response.text}')
                        raise Exception(f'{table_file} Table Submission Failed To Submit With {response.status_code}')



        except Exception as e:
            self.log.error(f'An Error Occurred: {str(e)}')
