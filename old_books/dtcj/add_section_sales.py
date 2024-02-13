import pandas as pd
import numpy as np
import datetime 

def add_section_sales(df, 
                      cat_col='Section Labels',
                      sales_col = 'SALES_VALUE',
                      id_col = 'household_key',
                         ) -> pd.DataFrame():
        
        
        ### accept a SalesTable object and return the sales broken down by a category, such as Section Labels
                                 ### could also be another product segmentation column
        
        idx = df.index
        # get dummies for each transaction row
        section_dummies = pd.get_dummies(df[cat_col])
#         print(all(section_dummies.index == idx))

        # multiply each row by it's SALES VALUE
        section_sales = section_dummies.apply(lambda x: x * df[sales_col])
        
#         print(all(section_sales.index == idx))
        
        return section_sales.join(df[id_col]).groupby(id_col).agg({col:sum for col in section_dummies.columns})
