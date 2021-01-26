1. Register Google Service Account with sheet api enabled
#Create application with https://console.developers.google.com/
#Click ENABLE API AND SERVICES
#Add Google SHEET API with search box
#Create SERVER credential(NOT Client)
#Download and Replace server_cred.json with your's
#Add scope choose gsheet/drive which not locked
#Share access to gsheet to email from server_cred.json

2. Installation
#change server_cred.json with your own
install deps with ./dev.sh

3. Launch with:
scrapy crawl spider

#Notes
- do not forget share document with email from server_cred.json
- sheet link https://docs.google.com/spreadsheets/d/foooooo/edit#gid=0
- has FILE_ID foo
