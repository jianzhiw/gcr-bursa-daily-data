from google.cloud import storage, bigquery
import logging
import os

class GCP:
    def __init__ (self):
        self.storage_client = storage.Client(project=os.getenv('PROJECT_ID'))
        self.bigquery_client = bigquery.Client(project=os.getenv('PROJECT_ID'))
    
    def create_bucket(self, bucket_name: str, project_id: str, region_name: str):
        """
            If bucket exist, then do nothing
            Else, create a bucket in GCP
        """

        bucket = self.storage_client.bucket(bucket_name)
        if bucket.exists():
            logging.info(f'Bucket { bucket_name } exist...')
            return None
        
        logging.info(f'Bucket { bucket_name } not exist, creating one...')
        bucket.create(client=self.storage_client, project=project_id, location=region_name)
        logging.info(f'Bucket { bucket_name } created...')
        return None

    def insert_data_from_dataframe(self, df, bigquery_schema, bigquery_table):
        """
            Insert data into BigQuery
        """
        logging.info(f'Inserting data into { bigquery_schema }.{ bigquery_table }...')
        table = self.bigquery_client.dataset(bigquery_schema).table(bigquery_table)
        self.bigquery_client.load_table_from_dataframe(df, table)
        logging.info(f'Data inserted into { bigquery_schema }.{ bigquery_table }...')
        return None

    def upload_storage(self, bucket_name, file_name, delete_file=True):
        """
            Upload flat file into GCS
        """
        logging.info(f'Uploading { file_name } into { bucket_name }...')
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_filename(file_name)
        logging.info(f'{ file_name } uploaded into { bucket_name }...')
        if delete_file == True:
            os.remove(file_name)
            logging.info(f'Deleted { file_name }...')

        return None