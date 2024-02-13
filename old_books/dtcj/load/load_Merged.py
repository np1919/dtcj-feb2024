import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# import os
import dtcj


class Merged:

    '''Wrapper for Table 1; Merged
    
    Loads clean data
    Properties:
        demographic households only;
        return a table of datetime versus household sales sum series
    
    I'd like to standardize to remove outliers across major sales analysis channels; to pop them into a review folder maybe. 
    
    '''    
    def __init__(self, 
                 sales_col='SALES_VALUE',
                 customer_id='household_key',
                 dt_col='datetime',
                 filepath=None):

        self.sales_col = sales_col
        self.customer_id =  customer_id
        self.dt_col = dt_col
        
        self.demo_list = dtcj.demo_list( )
        self.df = dtcj.load_merged()
        ''' ## LOADING self.df ## '''
        if filepath is not None:
            # if specified, load the clean table from outputs
            self.df = pd.read_csv(filepath)
            # as a default, load the table from scratch using load_merged module
        

#     @property    
    def demo_only(self):
        ''' ## FILTERING FOR DEMO HOUSEHOLDS ONLY '''
        return self.df[self.df['household_key'].isin(self.demo_list)]



    def sales_over_time(self, 
                            resample_rule = 'BQ',
                           ):
        '''return the sales series of `dt_col` resample sums for one or many `sales_col`; for one or many given `customer_id`s'''
        df = self.df
        customer_id=self.customer_id
        dt_col = self.dt_col
        sales_cols = self.sales_col
        hh_keys = list(self.df[customer_id].unique())

    #     print(type(hh_keys))
        ####
        fails = []
        output = pd.DataFrame()
        for hh in hh_keys:
            try:
                output=output.append(df[df[customer_id]==hh].resample(resample_rule, on=dt_col)[sales_cols].sum(), ignore_index=True)
            except:
                fails.append(hh)
                pass

    #     assert all(hh_keys == list(output.index)) ## what..don't pass thru constructor?
        if len(fails)>1:
            output.index = hh_keys ### SILENT ERROR
        return output
    #             .agg(**{x:'sum' for x in sales_cols}) ### ADD HOUSEHOLD KEY


        
#         self.df.resample(resample_rule, on=dt_col).groupby('household_key')