import pandas as pd
import numpy as np 


def RFM_Score(merged):
    last_days = merged.groupby('household_key')['DAY'].max()
    R = pd.cut(last_days, [0, 525, 615, 675, 700, np.inf], labels=[1,2,3,4,5], ordered=True)
    num_baskets = merged.groupby('household_key')['BASKET_ID'].nunique()
    grouper = merged.groupby('household_key')['DAY']
    days_in_data = grouper.max() - grouper.min() + 1 #(no day 0 in our data)
    transactions_per_day = num_baskets/days_in_data
    F = pd.qcut(transactions_per_day, 5, labels=[1,2,3,4,5])
    M = pd.qcut(np.log(merged.groupby('household_key')['SALES_VALUE'].sum()), 5, labels=[1,2,3,4,5])
    df = pd.concat([R, F, M], axis=1)
    df.columns = ['R', 'F', 'M']
    df['RFM'] = df.sum(axis=1).astype(int)
    customer_ranks = pd.cut(df['RFM'], bins=[0,6,9,13,15, np.inf], labels=[1,2,3,4,5], right=False).astype(int)
    customer_ranks = pd.DataFrame(customer_ranks) ## THIS IS HACKY BRO
    df['RFM Bins'] = customer_ranks

    return df