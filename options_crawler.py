import pandas as pd
import requests
from datetime import datetime, timedelta
import os
import sys


def fetch_options_data(start_date, end_date):
    url = 'https://www.taifex.com.tw/cht/3/pcRatio'
    data = {
        'down_type': '',
        'queryStartDate': start_date.strftime('%Y/%m/%d'),
        'queryEndDate': end_date.strftime('%Y/%m/%d')
    }
    result = requests.post(url=url, data=data)
    return pd.read_html(result.text)[0]


def get_date_ranges(start_date, end_date):
    date_ranges = []
    current_start = start_date
    while current_start <= end_date:
        current_end = min(current_start + timedelta(days=29), end_date)
        date_ranges.append((current_start, current_end))
        current_start = current_end + timedelta(days=1)
    return date_ranges


if __name__ == '__main__':
    options_file_name = 'options.pkl'
    if os.path.exists(options_file_name):
        old_pickle_file = pd.read_pickle(options_file_name)
        start_date = old_pickle_file.index[-1] + timedelta(days=1)
        print(f"Found existing data. Starting from {start_date.strftime('%Y/%m/%d')}")
    else:
        # 選擇權交易從 2001 年 12 月 24 日 開始成立
        start_date = datetime(2001, 12, 24)
        print("No existing data found. Starting from 2001-12-24")

    end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    if start_date > end_date:
        print("Data is up to date. No new data to fetch.")
        sys.exit(0)
    date_ranges = get_date_ranges(start_date, end_date)

    new_data = []
    for start, end in date_ranges:
        print(f"Fetching data from {start.strftime('%Y/%m/%d')} to {end.strftime('%Y/%m/%d')}")
        table = fetch_options_data(start, end)
        new_data.append(table)

    if len(new_data) == 0:
        print("No new data fetched.")
        sys.exit(0)
    new_result = pd.concat(new_data).reset_index(drop=True).set_index('日期')
    new_result.index = pd.to_datetime(new_result.index, format='%Y/%m/%d')

    final_result = new_result
    if os.path.exists(options_file_name):
        final_result = pd.concat([old_pickle_file, new_result])

    final_result = final_result[~final_result.index.duplicated(keep='last')]
    final_result = final_result.sort_index()
    final_result.to_pickle(options_file_name)

    print(f"Data fetching completed. {len(new_result)} new records added.")
    print(f"Total records: {len(final_result)}")
    print(f"Data saved to {options_file_name}")
