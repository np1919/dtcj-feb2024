import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt


def plot_campaign_sales(campaign_summary, camp_no, merged):
    fig, ax = plt.subplots(figsize=(16,4))
    
    plt.title(f'Sum of Sales for Products Listed in Campaign {camp_no} (Highlighted)')
    plt.ylabel(f'Avg. Daily Sales')
    plt.xlabel('DAY')    
    
    first = campaign_summary[camp_no]['First Day']
    last = campaign_summary[camp_no]['Last Day']
    total_days = campaign_summary[camp_no]['Duration']
    product_list = campaign_summary[camp_no]['Listed Products']
    ### How Much Data
    trans_max = merged['DAY'].max()
    trans_min = merged['DAY'].min()

    merged[merged['PRODUCT_ID'].isin(product_list)].groupby('DAY')['SALES_VALUE'].sum().plot(color='black', label=' Listed Products Sales')
    plt.axvspan(first, last, alpha=0.2, color='yellow')

    val = campaign_summary[camp_no]['Listed Products Sales During'] / (last - first) + 1
    ax.plot((first, last), (val, val) , color='red', label='Avg. during')

    val = campaign_summary[camp_no]['Listed Products Sales After'] / (trans_max - last) + 1
    ax.plot((last, trans_max), (val, val) , color='blue', label='Avg. after')

    val = campaign_summary[camp_no]['Listed Products Sales Before'] / (first - trans_min) + 1 
    ax.plot((trans_min, first), (val, val) , color='purple', label='Avg. before')

    val = campaign_summary[camp_no]['Listed Products Total Sales'] / ((trans_max - trans_min) +1)
    ax.plot((trans_min, trans_max), (val, val) , color='cyan', label='Avg. total', alpha=0.5)
    plt.legend()
    plt.show()
    