import datetime
import pandas as pd
import numpy as np

def days_between(df):
    '''take the .diff() of the sorted list of transaction dates for each household;
    round the mean of that and return a Series of all households in df
    '''
    days_between = dict()
    # loop through household_keys
    for key in df['household_key'].unique():

        # find the subset of transactions matching that household and  use .diff() to calculate the days between...
        # ...transactions; multiple transactions on the same day are ignored.
        a = pd.Series(df[df['household_key']==key]['DAY'].unique()).sort_values().diff()[1:]

        #calculate the mean difference between days of purchase
        days_between[key] = round(a.mean(), 2)


    ser = pd.Series(data=days_between.values(), index=days_between.keys())
#     ser.name = 'days_between_purchases'
    ser = pd.DataFrame(ser).reset_index()
    ser.columns=['household_key', 'days_between_purchases']
    return ser # included in the huge function below