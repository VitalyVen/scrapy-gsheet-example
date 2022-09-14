Pipeline (based on exporter) example
![image](https://user-images.githubusercontent.com/16899212/190243385-fd87f2ed-4238-4c1f-9877-ec277746c5d4.png)

# Register Google Service Account with sheet api enabled:

* Create application with https://console.developers.google.com/
* Click ENABLE API AND SERVICES
* Add Google SHEET API with search box
* Create SERVER credential(NOT Client)
* Download and Replace server_cred.json with your's
* Add scope choose gsheet/drive which not locked
* Share access to gsheet to email from server_cred.json

# Makefile
install, launch, test, lint with Makefile 

# Known bugs
clear only 1000 rows on start, and <30 colums, check it

# Notes
* do not forget share document with email from server_cred.json
* sheet link https://docs.google.com/spreadsheets/d/foooooo/edit#gid=0
* has FILE_ID foo
