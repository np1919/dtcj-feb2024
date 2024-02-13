import pandas as pd
import numpy as np
import dtcj
import datetime


def load_hh_agg(df) -> pd.DataFrame:
    '''accept the transactions (merged) table and return relevant house-level aggregations'''

    def make_hh_agg(df) -> pd.DataFrame:
        # group transactions by household key and aggregate:
        hh_agg = df.groupby('household_key').agg(

        # total spend 
            total_spend=pd.NamedAgg(column="SALES_VALUE", aggfunc="sum"),
        # the total loyalty discount  
            total_loyalty=pd.NamedAgg(column="RETAIL_DISC", aggfunc="sum"), 
        # the total coupon match discount  
            total_coupon=pd.NamedAgg(column="COUPON_MATCH_DISC", aggfunc="sum"),
        # total quantity of items purchased   
            total_quantity=pd.NamedAgg(column='QUANTITY', aggfunc="sum"),

        # the number of baskets  
            num_baskets=pd.NamedAgg(column='BASKET_ID', aggfunc='nunique'),
        # number of unique of items purchased   
            unique_products=pd.NamedAgg(column='PRODUCT_ID', aggfunc='nunique'),

        # first day of purchase
            first_purchase=pd.NamedAgg(column='DAY', aggfunc='min'),
        # last day of purchase
            last_purchase=pd.NamedAgg(column='DAY', aggfunc='max'), 
                                                                    )

        ### Deriving Avg. Basket Spend and Avg. Item Cost --

        # average basket spend
        hh_agg['avg_basket_spend'] = hh_agg['total_spend']/hh_agg['num_baskets']

        # average item cost (total spend/quantity)
        hh_agg['avg_item_cost'] = hh_agg['total_spend']/hh_agg['total_quantity']
        return hh_agg

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
        days_between_purchases = pd.DataFrame(data=days_between.items(), columns=['household_key', 'days_between_purchases'])
        #         ser.name = 'days_between_purchases'
        return days_between_purchases
    
    
    def get_section_sales(df) -> pd.DataFrame():
    
        idx = df.index
        # get dummies for each transaction row
        section_dummies = pd.get_dummies(df['Section Labels'])

        # multiply each row by it's SALES VALUE
        section_sales = section_dummies.apply(lambda x: x * df['SALES_VALUE'])
    #     print(all(section_sales.index == idx))
        # add and group by household key, sum all rows from the dummy columns
        section_sales = section_sales.join(df[['household_key']]).groupby('household_key').agg(sum)
        return section_sales

    def add_RFM(hh_agg):
        labels = range(1,6)
        output = pd.DataFrame(index=hh_agg.index)
    #     idx = hh_agg.index

        ### Recency
        arr = np.array(hh_agg['last_purchase'])
        arr = pd.qcut(np.ravel(arr), 5, labels=labels)
        output['R'] = arr.astype('int') # could easily be categorical

        ### Frequency
        arr = np.array(hh_agg['days_between_purchases'])
        arr = pd.qcut(np.ravel(arr), 5, labels=labels)
        output['F'] = arr.astype('int') # could easily be categorical

        ### Monetary
        arr = np.array(hh_agg['total_spend'])
        arr = pd.qcut(np.ravel(arr), 5, labels=labels)
        output['M'] = arr.astype('int') # could easily be categorical

        ### Sum to get final score
        output['RFM'] = output[['R', 'F', 'M']].astype(int).sum(axis=1)
        return output

    ### RUNTIME
    hh_agg = make_hh_agg(df)
    hh_agg = hh_agg.merge(days_between(df), left_index=True, right_index=True)
    hh_agg = hh_agg.merge(dtcj.get_section_sales(df),  left_index=True, right_index=True)
    hh_agg = hh_agg.merge(add_RFM(hh_agg), left_index=True, right_index=True)
    return hh_agg
