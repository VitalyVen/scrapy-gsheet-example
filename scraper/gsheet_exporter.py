import google.auth.transport.requests
import google.oauth2.credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from scrapy.exporters import CsvItemExporter
from scrapy.utils.python import to_native_str

request_transport = google.auth.transport.requests.Request
from google.auth.transport.requests import Request


def get_credentials_from_service_account(scopes: list, service_account_path: str):
    creds = service_account.Credentials.from_service_account_file(service_account_path, scopes=scopes)

    creds.refresh(Request())  # bug
    creds.refresh(Request())  # bug
    return creds


class GSheetExporter(CsvItemExporter):
    def __init__(self, creds, file_id, include_headers_line=True, join_multivalued=",", **kwargs):
        self._configure(kwargs, dont_fail=True)
        if not self.encoding:
            self.encoding = "utf-8"
        self.include_headers_line = include_headers_line
        self._headers_not_written = True
        self._join_multivalued = join_multivalued
        self.service = build("sheets", "v4", credentials=creds)
        self.file_id = file_id
        self.rows_cache = []  # there are no big data, it should be ok)

    def export_item(self, item) -> None:
        if self._headers_not_written:
            self._headers_not_written = False
            self._write_headers_and_set_fields_to_export(item)

        fields = self._get_serialized_fields(item, default_value="", include_empty=True)
        values = list(self._build_row(x for _, x in fields))
        self.rows_cache.append(values)

    def write_rows_cache(self) -> None:
        values = [list(row) for row in self.rows_cache]
        range_name = "A1:C{}".format(len(self.rows_cache) + 1)
        body = {"values": values}
        result = (
            self.service.spreadsheets()
            .values()
            .update(spreadsheetId=self.file_id, range=range_name, valueInputOption="RAW", body=body)  # USER_ENTERED
            .execute()
        )
        print("{0} cells updated.".format(result.get("updatedCells")))

    def _build_row(self, values):
        for s in values:
            try:
                yield to_native_str(s, self.encoding)
            except TypeError:
                yield s

    def start_exporting(self) -> None:
        range_name = "A:K".format()  # 1000 rows default # TODO: handle not default rows
        self.service.spreadsheets().values().clear(spreadsheetId=self.file_id, range=range_name).execute()
        super(GSheetExporter, self).start_exporting()

    def finish_exporting(self) -> None:
        self.write_rows_cache()
        super(GSheetExporter, self).finish_exporting()

    def _write_headers_and_set_fields_to_export(self, item) -> None:
        if self.include_headers_line:
            if not self.fields_to_export:
                if isinstance(item, dict):
                    # for dicts try using fields of the first item
                    self.fields_to_export = list(item.keys())
                else:
                    # use fields declared in Item
                    self.fields_to_export = list(item.fields.keys())
            row = list(self._build_row(self.fields_to_export))
            self.rows_cache.append(row)


if __name__ == "__main__":
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = get_credentials_from_service_account(scopes=SCOPES, service_account_path="../server_cred.json")
    creds.refresh(Request())  # bug
    creds.refresh(Request())  # bug
    service = build("sheets", "v4", credentials=creds)
    range_name = "A:K".format()  # 1000 rows default
    service.spreadsheets().values().clear(
        spreadsheetId="1Jy35Mg3AjAWziCSfUcHrujQlV7vnPfZQGgBH1KbZfYY", range=range_name
    ).execute()
