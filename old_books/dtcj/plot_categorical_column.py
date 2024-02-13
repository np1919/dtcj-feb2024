import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_categorical_column(demo, 
                            merged,
                            mean=True,
                            resample_rule='BM',
                            sales_col='SALES_VALUE',
                            label_col='HOUSEHOLD_SIZE_DESC',
                           id_col='household_key'):
    
    fig, ax = plt.subplots(figsize=(16,6))
    if mean==True:
        plt.title(f'Mean Sum of {sales_col} by {label_col}; over {resample_rule}')
    elif mean==False:
        plt.title(f'Sum of {sales_col} by {label_col}; over {resample_rule}')
        
    for size in demo[label_col].unique():
        hh_ids = list(demo[demo[label_col]==size][id_col])
        
        if mean==True: # divide by len(hh_ids)
            ax.plot((merged[merged[id_col].isin(hh_ids)].resample(resample_rule,convention='end', on='datetime')[sales_col].sum()/len(hh_ids)), label=f'{size}')
        else:
            ax.plot(merged[merged[id_col].isin(hh_ids)].resample(resample_rule,convention='end', on='datetime')[sales_col].sum(), label=f'{size}')

    
    plt.legend()
    plt.show()