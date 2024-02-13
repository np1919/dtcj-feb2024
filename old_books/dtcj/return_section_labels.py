import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import pickle


def return_section_labels(df, file_loc='Section_Labels.txt'):
    with open('Section_Labels.txt', 'r') as f:
        d = eval(f.readlines()[0])
    ser = df['COMMODITY_DESC'].map(d) # hardcoded;
    ser = ser.fillna('misc') # for exceptions ?
    return ser