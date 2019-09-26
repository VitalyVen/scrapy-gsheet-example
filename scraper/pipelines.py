# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import configparser
from .gsheet_exporter import GSheetExporter, get_credentials_from_service_account

config = configparser.ConfigParser()
config.read('scrapy.cfg')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_PATH = config['GSHEET']['SERVICE_ACCOUNT_PATH']
GSHEET_FILE_ID = config['GSHEET']['GSHEET_FILE_ID']

class ScraperPipeline(object):
    def __init__(self, file_name=None):
        # Storing output filename
        self.file_id = file_name
        self.file_id = None
        self.creds = get_credentials_from_service_account(scopes=SCOPES, service_account_path=SERVICE_ACCOUNT_PATH)
        self.exporter = GSheetExporter(self.creds, GSHEET_FILE_ID)

    def open_spider(self, spider):
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
