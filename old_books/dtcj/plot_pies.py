import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import pickle


def plot_pies(df, drop_columns=None): # kwargs for subplots call?
    

    if drop_columns:
        columns = df.columns.drop(drop_columns) 
    else:
        columns = df.columns
    rows = 4

    plt.subplots(len(columns)//rows+1, rows, figsize=(16,8))
    for idx, col in enumerate(columns):

        plt.subplot(len(columns)//rows+1, rows, idx+1)
        plt.title(f'{col}')
        counts = df[col].value_counts()
        plt.pie(counts, labels=counts.index, autopct='%1.1f%%',) #makes the MARITAL_STATUS_CODE column disappear..?
    plt.tight_layout()
    plt.show()
 