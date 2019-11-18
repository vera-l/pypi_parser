#!/usr/bin/env python3

from config import Config
from data_service import DataService

from parser import run

import logging
logging.basicConfig(level=logging.INFO, filename='parse.log')

if __name__ == '__main__':
    config = Config()
    data_service = DataService(
        config.get('db_connection_url'),
        config.get('db_name'),
    )
    run(config.get('start_url'), data_service)
