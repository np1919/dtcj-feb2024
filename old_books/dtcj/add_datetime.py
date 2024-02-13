import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime


def add_datetime(df):

    def make_date_map(df, dates='DAY'):
        # 'DAY' 1 == 2004-03-23
        day1 = datetime.datetime(2004, 3, 23) # as derived in transactions notebook; datetime for 'DAY' == 1
        ineedthismany = df[dates].max()
        last = day1 + datetime.timedelta(days=int(ineedthismany))
        date_range = pd.date_range(day1, last) # date range for our data
        # map datetime index to DAY; enumerate() indexes from 0, so we add 1
        date_map = {i+1:x for i, x in enumerate(date_range)}

        output = df[dates].map(date_map)
        output = pd.to_datetime(output)
        return output

    def make_time_map(df, times='TRANS_TIME'):
        ''''''
        # pad zeros
        output = df[times].astype(str).str.zfill(4)

        # split to hours and minutes
        hours = output.str[:2]
        minutes = output.str[2:]

        # convert to timedelta
        hours = pd.to_timedelta(hours.astype('int'), unit='hour')
        minutes = pd.to_timedelta(minutes.astype('int'), unit='minute')
        output = hours + minutes
        return output
    
    return make_date_map(df) + make_time_map(df)
