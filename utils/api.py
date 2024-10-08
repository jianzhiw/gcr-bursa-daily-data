import requests
import camelot
import logging
from datetime import datetime, date
from PyPDF2 import PdfReader
import pandas as pd

class API():
    def __init__(self):
        self.bursa_status = ''
        self.file_name = ''
        self.pdf_date = ''
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 OPR/92.0.0.0'}
    
    def get_bursa_daily_data(self, pdf_date):
        """
        Get pdf file from https://www.bursamalaysia.com/misc/missftp/securities/yyyy-mm-dd.pdf
        date must be in yyyy-mm-dd format
        """

        url = 'https://www.bursamalaysia.com/misc/missftp/securities/'
        date_format = '%Y-%m-%d'
        try:
            datetime.strptime(pdf_date, date_format)
        except ValueError as e:
            e('Date format should be YYYY-MM-DD')
            logging.error(f'Expected date format { date_format }, input { pdf_date }...')
            return None

        self.pdf_date = pdf_date
        self.file_name = f'securities_equities_{ pdf_date }.pdf'
        logging.info(f'Getting data from { url }{ self.file_name }...')
        r = requests.get(f'{ url }{ self.file_name }', headers=self.headers)

        self.bursa_status = r.status_code
        if r.status_code != 200:
            logging.error(f'HTTP return { r.status_code }...')
            return None
        
        logging.info(f'Writing data into { self.file_name }...')
        with open(self.file_name, 'wb') as f:
            f.write(r.content)
        
        logging.info('Function get_bursa_daily_data executed!')
        return None
    
    def get_bursa_daily_data_v2(self, pdf_date):
        """
        Get pdf file from https://www.bursamalaysia.com/misc/missftp/securities/securities_equities_daily_scoreboard_yyyymmdd.pdf
        date must be in yyyymmdd format
        """

        self.pdf_date = pdf_date
        url = 'https://www.bursamalaysia.com/misc/missftp/securities/'
        date_format = '%Y%m%d'
        try:
            datetime.strptime(pdf_date, date_format)
        except ValueError as e:
            e('Date format should be YYYYMMDD')
            logging.error(f'Expected date format { date_format }, input { pdf_date }...')
            return None
        
        self.file_name = f'securities_equities_daily_scoreboard_{ pdf_date }.pdf'
        logging.info(f'Getting data from { url }{ self.file_name }...')
        r = requests.get(f'{ url }{ self.file_name }', headers=self.headers)

        self.bursa_status = r.status_code
        if r.status_code != 200:
            logging.error(f'HTTP return { r.status_code }...')
            return None
        
        logging.info(f'Writing data into { self.file_name }...')
        with open(self.file_name, 'wb') as f:
            f.write(r.content)
        
        logging.info('Function get_bursa_daily_data executed!')
        return None
    
    def generate_bursa_daily_data(self):
        """
        Generate bursa_daily_data DataFrame
        """

        header = 'Date Stock\nCodeStock Name Cur. Opening\nPriceHigh\nPriceLow\nPriceClosing\nPriceVolume\nTraded -\nMarket\nTransactionValue Traded\n- Market\nTransaction\n(RM)\n'
        footer = 'Daily Stock Transaction'
        columns = ['date', 'stock_code', 'stock_name', 'currency', 'open', 'high', 'low', 'close', 'volume', 'market_transaction_value']
        list = []

        if self.file_name == '':
            logging.error('Missing file to generate data. Please run get_bursa_daily_data() first...')
            return None
        
        logging.info(f'Generating data from { self.file_name }')
        pdf = PdfReader(self.file_name)
        for page in pdf.pages:
            text = page.extract_text()
            if header in text:
                clean_text = text.replace(header, '').split(footer)[0]
                list.extend([x.replace(',', '').replace('#', '0') for x in y.split(' ')] for y in clean_text.split('\n'))

        logging.info(f'Converting data into DataFrame...')
        df = pd.DataFrame(list, columns=columns)
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
        df['ingestion_date'] = date.today()
        convert = {
            'date': 'datetime64[ns]',
            'open': 'float64',
            'high': 'float64',
            'low': 'float64',
            'close': 'float64',
            'volume': 'int64',
            'market_transaction_value': 'int64',
            'ingestion_date': 'datetime64[ns]'
        }
        df = df.astype(convert)

        logging.info('Function generate_bursa_daily_data executed!')
        return df
    
    def generate_bursa_daily_data_v2(self, page_numbers='7-end', line_scale=30):
        """
        Generate bursa_daily_data DataFrame
        """

        columns = {
            0: 'stock_code', 
            1: 'stock_name', 
            2: 'currency', 
            3: 'open', 
            4: 'high', 
            5: 'low', 
            6: 'close', 
            7: 'volume', 
            8: 'market_transaction_value'
        }

        convert = {
            'date': 'datetime64[ns]',
            'open': 'float64',
            'high': 'float64',
            'low': 'float64',
            'close': 'float64',
            'volume': 'int64',
            'market_transaction_value': 'int64',
            'ingestion_date': 'datetime64[ns]'
        }

        df = pd.DataFrame()

        if self.file_name == '':
            logging.error('Missing file to generate data. Please run get_bursa_daily_data() first...')
            return None
        
        logging.info(f'Generating data from { self.file_name }')
        pdf_tables = camelot.read_pdf(self.file_name, pages=page_numbers, line_scale=line_scale)
        for table in pdf_tables:
            df = pd.concat([df, table.df], axis=0)

        logging.info(f'Converting data into DataFrame...')
        
        df = df.rename(columns=columns)
        df['date'] = pd.to_datetime(datetime.strptime(self.pdf_date, '%Y%m%d'), format='%d/%m/%Y')
        df['volume'] = df['volume'].replace(',', '')
        df['volume'] = df['volume'].replace(regex=r'\,', value='')
        df['market_transaction_value'] = df['market_transaction_value'].replace(regex=r'\,', value='')
        df['ingestion_date'] = date.today()
        df = df.astype(convert)

        logging.info('Function generate_bursa_daily_data executed!')
        return df