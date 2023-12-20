import os
import sys
import logging

class Helper():
    def __init__ (self):
        self.version = 'v0.1'
        self.initialize_logging()
    
    def initialize_logging(self):
        """
        Initialize Logging
        """

        logging.basicConfig(format='%(asctime)s - %(levelname)-8s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S %z', stream=sys.stdout)
        log = logging.getLogger()
        log.setLevel(logging.INFO)
        
        return None

    def generate_requirements(self, ignore_directories: str):
        """
        Generate requirements.txt
        """
        logging.info('Generating requirements.txt...')
        os.system(f'pipreqs --force --ignore={ ignore_directories } --encoding=utf8 .')
        logging.info('requirements.txt generated...')

        return None

    def build_docker(self, tag: str, test: str = False):
        """
        Build docker image
        """
        logging.info(f'Building docker image { tag }... test = { test }')

        if os.path.exists('./Dockerfile') == False:
            logging.error('Dockerfile does not exist. Build fail...')
            return None

        if test == 'True':
            os.system(f'docker build --tag { tag } .')
        else:
            os.system(f'docker build --tag { tag } . --platform linux/amd64')
        logging.info(f'Docker image { tag } built...')

        return None
    
    def run_docker(self, tag: str):
        """
        Run docker in test
        """
        logging.info(f'Running docker image { tag }...')
        return os.system(f'docker run -p 8080:8080 { tag }')
