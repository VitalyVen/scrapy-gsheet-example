import os
from pathlib import Path

SPIDER_MODULES = ["scraper.spiders"]
NEWSPIDER_MODULE = "scraper.spiders"
# GSHEET
GSHEET_SERVICE_ACCOUNT_PATH = Path(__file__).parent.parent / "server_cred.json"
GSHEET_FILE_ID = os.getenv("GSHEET_FILE_ID")
assert GSHEET_FILE_ID
