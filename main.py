import os
from flask import Flask
from utils.helper import Helper
from utils.api import API
from utils.gcp import GCP
import logging
from datetime import date

app = Flask(__name__)
helper = Helper()
gcp = GCP()
api = API()

@app.route('/')
def hello_world():
    logging.info('Sending Hello World!...')
    return 'Hello World!'

@app.route('/bursa_daily_data', methods=['GET'])
def get_bursa_daily_data():
    logging.info('Executing get_bursa_daily_data...')
    pdf_date = date.today().strftime('%Y-%m-%d')
    api.get_bursa_daily_data(pdf_date=pdf_date)

    if api.bursa_status == 200 and api.file_name != '':
        logging.info(f'Bursa status { api.bursa_status }...')
        logging.info(f'Downloaded { api.file_name }...')
        df = api.generate_bursa_daily_data()
        gcp.insert_data_from_dataframe(df, bigquery_schema=os.getenv('GBQ_SCHEMA_STOCK'), bigquery_table=os.getenv('GBQ_TABLE_STOCK'))
        gcp.upload_storage(bucket_name=os.getenv('GCS_BUCKET_STOCK'), file_name=api.file_name, delete_file=True)
    
    logging.info('get_bursa_daily_data executed!')
    return 'bursa_daily_data executed!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)