import numpy as np
import pandas as pd

def demo_map_categorical(demo=pd.read_csv('data/hh_demographic.csv')):
    demo['AGE_DESC'] = pd.Categorical(demo['AGE_DESC'], ['19-24', '25-34','35-44',  '45-54', '55-64',  '65+',])

    demo['MARITAL_STATUS_CODE'] = pd.Categorical(demo['MARITAL_STATUS_CODE'].map({'A':'Married', 'B':'Single', 'U': 'Unknown'}), ['Married', 'Single', 'Unknown'], ordered=False)

    demo['INCOME_DESC']= pd.Categorical(demo['INCOME_DESC'], ['Under 15K','15-24K','25-34K', '35-49K', '50-74K','75-99K',  
           '100-124K', '125-149K', '150-174K', '175-199K', '200-249K','250K+', ])

    demo['HOMEOWNER_DESC']= pd.Categorical(demo['HOMEOWNER_DESC'], ['Homeowner', 'Unknown', 'Renter', 'Probable Renter', 'Probable Owner'], ordered=False)

    demo['HH_COMP_DESC']=pd.Categorical(demo['HH_COMP_DESC'], ['Single Female', 'Single Male', '1 Adult Kids','2 Adults No Kids', '2 Adults Kids', 'Unknown',], ordered=False)
    demo['HOUSEHOLD_SIZE_DESC'] = pd.Categorical(demo['HOUSEHOLD_SIZE_DESC'], ['1', '2','3','4','5+',])
    demo['KID_CATEGORY_DESC']=pd.Categorical(demo['KID_CATEGORY_DESC'], ['1','2','3+','None/Unknown', ])
    
    return demo