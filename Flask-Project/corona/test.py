from datetime import date, timedelta
from pprint import pprint
import corona_data

now = date.today()
now_str = now.strftime("%Y%m%d")

data = corona_data.get_corona_data('20210425', '20210425')
# pprint(data)
# print(data)
if not data:
    yesterday = now - timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y%m%d')
    print(yesterday_str)

    data = corona_data.get_corona_data(yesterday_str, yesterday_str)
    pprint(data)
