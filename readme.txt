enviroment:
conda : mednetserver
python : 3.8

db server 
使用postgresql port:5432

superuser
systemadmin
nlp8B417

每增加新的user 進來的時候，要將伺服器重開，讓他讀進去user的model

執行方式到 C:/Apache24/bin/
用系統管理員開起cmd

安裝一個叫 "apache" 的伺服器
>> httpd.exe -k install -n “apache”

解安裝一個叫 "apache" 的伺服器
>> httpd.exe -k uninstall -n “apache”


關閉apache server
>> sc stop "apache"
開啟apache server
>> sc start "apache"


