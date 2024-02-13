import pandas as pd
import numpy as np

def load_demo():
    demo = pd.read_csv('data/hh_demographic.csv')
    
    ## Apply Categorical Ranks
#     demo['AGE_DESC'] = pd.Categorical(demo['AGE_DESC'], ['19-24', '25-34','35-44',  '45-54', '55-64',  '65+',])

#     demo['MARITAL_STATUS_CODE'] = pd.Categorical(demo['MARITAL_STATUS_CODE'].map({'A':'Married', 'B':'Single', 'U': 'Unknown'}), ['Married', 'Single', 'Unknown'])

#     demo['INCOME_DESC']= pd.Categorical(demo['INCOME_DESC'], ['Under 15K','15-24K','25-34K', '35-49K', '50-74K','75-99K',  
#        '100-124K', '125-149K', '150-174K', '175-199K', '200-249K','250K+', ])

#     demo['HOMEOWNER_DESC']= pd.Categorical(demo['HOMEOWNER_DESC'], ['Homeowner', 'Unknown', 'Renter', 'Probable Renter', 'Probable Owner'], ordered=False)

#     demo['HH_COMP_DESC']=pd.Categorical(demo['HH_COMP_DESC'], ['Unknown', 'Single Female', 'Single Male', '1 Adult Kids','2 Adults No Kids', '2 Adults Kids'], ordered=False)
#     demo['HOUSEHOLD_SIZE_DESC'] = pd.Categorical(demo['HOUSEHOLD_SIZE_DESC'], ['1', '2','3','4','5+',])
#     demo['KID_CATEGORY_DESC']=pd.Categorical(demo['KID_CATEGORY_DESC'], ['None/Unknown', '1','2','3+',])
    
    
    ## Alternate Mappings
    demo['age_45+'] = demo['AGE_DESC'].map({ '19-24':0,
                                            '25-34':0,
                                            "35-44":0,
                                            '45-54':1,
                                            '55-64':1,
                                            '65+':1,
                                            })
    

    demo['income_50K+'] = demo['INCOME_DESC'].map({
                            'Under 15K': 0,
                             '15-24K': 0,
                             '25-34K': 0,
                             '35-49K': 0,
                             '50-74K': 1,
                             '75-99K': 1,
                             '100-124K': 1,
                             '125-149K': 1,
                             '150-174K': 1,                   
                             '175-199K': 1,  
                             '200-249K': 1,
                             '250K+': 1,
                            })
    
    # leaving household_size desc IN as a category; single, couple, 3+
    demo['single_couple_family'] = demo['HOUSEHOLD_SIZE_DESC'].map({'1':1, '2':2, '3':3,'4':3,'5+':3})
    demo['single_couple_family'] = pd.Categorical(demo['single_couple_family'], 
                                                 [1,2,3,])

     
#    
    demo['has_kids'] = np.where((demo['HH_COMP_DESC'] == '1 Adult Kids') |
                               (demo['HH_COMP_DESC'] == '2 Adults Kids') |
                                (demo['HOUSEHOLD_SIZE_DESC'].isin(['3', '4', '5+'])),
                                1, 0)
    
    demo['single'] =  np.where((demo['HH_COMP_DESC'] == 'Single Female') |
                               (demo['HH_COMP_DESC'] == 'Single Male') |
                               (demo['HOUSEHOLD_SIZE_DESC'] == '1'),
                                1, 0)
    
    demo['couple'] =  np.where((demo['HH_COMP_DESC'] == '2 Adults No Kids'),
                                1, 0)
    
    demo = demo.drop(['AGE_DESC', 'MARITAL_STATUS_CODE', 
               'INCOME_DESC', 'HOMEOWNER_DESC', 'HH_COMP_DESC', 
               'HOUSEHOLD_SIZE_DESC', 'KID_CATEGORY_DESC'], axis=1)
    return demo
                       