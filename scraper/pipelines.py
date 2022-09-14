from scrapy import Spider
from scrapy.utils.project import get_project_settings

from scraper.gsheet_exporter import (GSheetExporter,
                                     get_credentials_from_service_account)

settings = get_project_settings()

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SERVICE_ACCOUNT_PATH = settings["GSHEET_SERVICE_ACCOUNT_PATH"]
GSHEET_FILE_ID = settings["GSHEET_FILE_ID"]


class ScraperPipeline:
    def __init__(self, file_name: str | None = None) -> None:
        # Storing output filename
        self.file_id = file_name
        self.file_id = None
        self.creds = get_credentials_from_service_account(scopes=SCOPES, service_account_path=str(SERVICE_ACCOUNT_PATH))
        self.exporter = GSheetExporter(self.creds, GSHEET_FILE_ID)  # type: ignore

    def open_spider(self, spider: Spider) -> None:  # pylint:disable=unused-argument
        self.exporter.start_exporting()

    def close_spider(self, spider: Spider) -> None:
        self.exporter.finish_exporting()

    def process_item(self, item, spider: Spider):  # type: ignore
        self.exporter.export_item(item)
        return item
