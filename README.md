# 臺指選擇權Put/Call比爬蟲
到 https://www.taifex.com.tw/cht/3/pcRatio 爬取臺指選擇權 Put / Call 比的資料，並將資料存入 options.pkl 檔


## 使用說明

第一次使用時，請輸入 `pip install -r requirements.txt` 安裝相關的 python modules。

之後輸入 `python options_crawler` 即可爬取選擇權 2001/12/24 開始的資料。

程式執行時，會判斷 options.pkl 檔是否存在，若存在，則會從上次爬取的日期開始下載資料，並將資料整合到 options.pkl 內；若 options.pkl 不存在，則會從 2001/12/24 開始下載資料，然後再存到 options.pkl。