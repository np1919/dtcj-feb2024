import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt

import my_funcs as mf
import os

def ETL(new_directory='data/outputs'):
    ''' call all ETL functions and populate the /outputs directory in the main folder'''
    os.makedirs(new_directory)
    # first level
#     for function in ['load_demo','load_campaign_summary', 'load_merged']:
#         df = eval(f'mf.{function}()')
#         df.to_csv(f'TESToutputs/{function[5:]}.csv')
    
    df = mf.load_demo()
    df.to_csv(f'{new_directory}/demo.csv')
    
    merged = mf.load_merged()
    merged.to_csv(f'{new_directory}/merged.csv')
    
    df = mf.load_hh_agg(merged)
    df.to_csv(f'{new_directory}/hh_agg.csv')
    
    df = mf.load_campaign_summary(merged)
    df.to_csv(f'{new_directory}/campaign_summary.csv')

    return None
