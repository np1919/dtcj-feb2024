import pandas as pd
import numpy as np
import datetime



def load_hh_agg(df) -> pd.DataFrame:
    '''accept the merged table or a subset thereof and return relevant house-level aggregations'''

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


    def add_RFM(merged):
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
    
   
    def transformed_section_sales(merged):
        
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
        
        # create section sales
        section_sales = get_section_sales(merged)
        
       # log_transformed sum of section sales
        log_transformed_section_sales = np.log(section_sales).replace([np.inf, -np.inf], np.nan).fillna(0)
        log_transformed_section_sales.columns = [x + '_log_transformed_sales_total' for x in log_transformed_section_sales.columns]

        # daily mean spend per section 
        # based on # of days in data;
        # add Days in Data for each household; similar to Frequency transformation
        grouper = merged.groupby('household_key')['DAY']
        duration = (grouper.max() - grouper.min()) + 1 # no day 0
        duration.name = 'Days in Data'
        # divide each column by the household's Days in Data value
        test = section_sales.merge(duration, on='household_key').drop('Days in Data', axis=1)
        daily_mean_spend_per_category = test.div(duration, axis=0)
        daily_mean_spend_per_category.columns = [x + '_daily_mean_spend_per_category' for x in daily_mean_spend_per_category.columns]
        return pd.concat([log_transformed_section_sales, daily_mean_spend_per_category], axis=1)
      
    ### RUNTIME
    
    hh_agg = pd.concat([make_hh_agg(df), transformed_section_sales(df), add_RFM(df)], axis=1)

    return hh_agg
