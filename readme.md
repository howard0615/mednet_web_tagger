# 醫聯網資料摘要標記網頁

## 使用的package
* Django

## 描述
* 此網頁所標記資料來源為[醫聯網](https://med-net.com/)，藉由爬蟲將資料爬取。
* 此網頁主要任務將民眾所詢問的問題，摘要成較短的問句，利於之後問題理解的任務。

## Django網站設定

1. 將此repo下載至local端
```bash
git clone https://github.com/howard0615/mednet_web_tagger.git
```
2. 更改設定內容
    * 開啟 `mednet_sum_site/settings.py` 可更改
    * 若想使用 [PostgreSQL](https://www.postgresql.org/) 作為資料庫，可使用內容有Postgres `DATABASES` 的設定
    * 若想修改網頁內容，撰寫過程中可將 `DEBUG = True`

3. 建立migrations
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. 建立管理者
    * 管理者權限：後台管理資料、管理標記者、分配摘要與標記任務
    ```bash
    python manage.py createsuperuser
    ```

5. 測試 Django 網站
    ```bash
    python manage.py runserver
    ```
    * 至瀏覽器 `localhost:8000` 檢視網頁

6. 新增標記者
    * 至 `localhost:8000/admin/` 以 superuser 登入，並可在使用者處加入使用者資訊  
    Note : 新增新的使用者後，要重新開伺服器，使其可以讀取到使用者

## 介面使用方式
<<<<<<< HEAD
* 登入  
   ![text](https://github.com/howard0615/mednet_web_tagger/blob/master/img/login_page.png)
### SuperUser 管理員
* 
=======
* 登入
![login]('https://github.com/howard0615/mednet_web_tagger/blob/master/img/login_page.png')

### SuperUser 管理員
* 指派摘要任務給標記者  
![assemble_summarization]('https://github.com/howard0615/mednet_web_tagger/blob/master/img/superuser_assemblesummmarization_page.png')

* 指派摘要評分(label)給標記者  
![assemble_labe]('https://github.com/howard0615/mednet_web_tagger/blob/master/img/superuser_assemblelabel_page.png')

* 資料狀態
![data_condition]('https://github.com/howard0615/mednet_web_tagger/blob/master/img/superuser_data_condition.png')

* 將目前資料下載從 `localhost:8000/data/download_file/` (要先以superuser的身份登入)

123