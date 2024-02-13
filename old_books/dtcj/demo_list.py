import pandas as pd
import numpy as np
                       

def demo_list(filepath='data/hh_demographic.csv', 
                     id_col='household_key',
                    ):
    demo = pd.read_csv(filepath)
    lst= list(demo[id_col].unique())

    return lst