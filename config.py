#!/usr/bin/env python3
import configparser


class Config:
    def __init__(self, file='config.cfg'):
        config = configparser.RawConfigParser()
        config.read(file)
        self.values = {
            'db_connection_url': config.get('Database', 'connection_url'),
            'db_name': config.get('Database', 'db_name'),
            'start_url': config.get('Parsing', 'url'),
            'port': config.get('Server', 'port'),
        }

    def get(self, name):
        return self.values.get(name)
