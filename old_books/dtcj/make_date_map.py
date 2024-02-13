import datetime
import pandas as pd
import numpy as np

def make_date_map(df, last_day_column) -> dict:
    '''return a dictionary '''
    # 'DAY' 1 == 2004-03-23
    day1 = datetime.datetime(2004, 3, 23) # as derived in transactions notebook; datetime for 'DAY' == 1
    ineedthismany = df[last_day_column].max()
    last = day1 + datetime.timedelta(days=int(ineedthismany)- 1)   
    date_range = pd.date_range(day1, last) # date range for our data
    # map datetime index to DAY; enumerate() indexes from 0, so we add 1
    date_map = {i+1:x for i, x in enumerate(date_range)}

    output = df[last_day_column].map(date_map)
    output = pd.to_datetime(output)
    return date_map
