import datetime
import pandas as pd
import numpy as np
import dtcj

def load_merged(trans=None, prod=None) -> pd.DataFrame():
    if not trans:
        trans = pd.read_csv('data/transaction_data.csv')
        
    if not prod:
        prod = pd.read_csv('data/product.csv')
   

    trans['datetime'] = dtcj.add_datetime(trans)
#     prod['Section Labels'] = dtcj.return_section_labels(products)
    
    # Remove Empty Sales Rows
    trans = trans[(trans['QUANTITY'] > 0) & 
                  (trans['SALES_VALUE'] > 0)]
    
#     empty_rows = transactions[(transactions['SALES_VALUE'] == 0) & 
#                               (transactions['RETAIL_DISC']==0) &
#                               (transactions['COUPON_DISC']==0) &
#                               (transactions['COUPON_MATCH_DISC']==0)
#                              ]

    # Remove monthly/quarterly tails...
    trans = trans[(trans['datetime'] >= "2004-7-1") &
                  (trans['datetime'] < "2006-3-1")]
    
                   
    # Merge
    merged = trans.merge(prod.drop('CURR_SIZE_OF_PRODUCT', axis=1))
    
    # Remove Gasoline Sales
    merged.drop(merged[merged['SUB_COMMODITY_DESC']=='GASOLINE-REG UNLEADED'].index, axis=0, inplace=True)
    merged.drop(merged[merged['COMMODITY_DESC']=='GASOLINE-REG UNLEADED'].index, axis=0, inplace=True)
    
    # Add section labels
    merged['Section Labels'] = dtcj.return_section_labels(merged)
    
    # Remove one-day transactions
    def one_day_transactions(df) -> list:
        no_days = df.groupby('household_key').agg({'DAY':'nunique'})
        return list(no_days[no_days['DAY'] == 1].index)
        
    # remove households with only 1 day of purchases;
    merged = merged[~merged['household_key'].isin(one_day_transactions(merged))]    
    return merged.reset_index().drop('index', axis=1)
