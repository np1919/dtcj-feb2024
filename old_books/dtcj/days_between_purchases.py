import pandas as pd
import numpy as np


def days_between_purchases(df, 
                           id_col='household_key', 
                           date_col='DAY'):
    ''' return the `DAY`s between purchases for each 'household_key' in df;
        
        calculated using .diff(); returns inf for households with only one day of purchases
            returns the mean of the .diff() series; taken as the difference between each unique `date_col` value; rounded to 2 decimal places
        
    '''
    days_between_purchases = dict()
    # loop through household_keys
    for key in df['household_key'].unique():

        # find the subset of transactions matching that household and  use .diff() to calculate the days between...
        # ...transactions; multiple transactions on the same day are ignored.
        a = pd.Series(df[df[id_col]==key][date_col].unique()).sort_values().diff()[1:]

        #calculate the mean difference between days of purchase
        days_between_purchases[key] = round(a.mean(), 2)
    days_between_purchases = pd.DataFrame(data=days_between_purchases.items(), columns=['household_key', 'days_between_purchases'])
    #         ser.name = 'days_between_purchases'
    return days_between_purchases

