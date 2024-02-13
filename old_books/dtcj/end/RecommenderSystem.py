import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import pickle
import my_funcs

from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from mlxtend.frequent_patterns import fpgrowth

merged = pd.read_csv('../../outputs/merged.csv')

class RecommenderSystem:
    '''
    ## hh_key :  the household_key
    ## df : the transactions df; 
    ## column : the column in df to be used for MBA ('COMMODITY_DESC, DEPARTMENT, SUB_COMMODITY_DESC')
    ## max_len :  max length of any antecedent/consequent chains in support_table
    ## support_threshold : minimum 'support' threshold to generate fpgrowth
    
    ## metric : the association rules metric to maximize
    ## assoc_threshold : the association rules threshold, given the metric.
    '''
        ## Instantiate Class

    def __init__(self, 
                 hh_key,   ### FOR HOUSEHOLDS#!### 
                 df=merged, 
                 column='COMMODITY_DESC', 
                    max_len=None, ### CONSIDER REDUCING THIS VALUE FOR SIMPLICITY ###
                 support_threshold=0.05, ### WITH DATA OF FIXED SIZE, NOT A CONCERN? ###
                metric='confidence', 
                 assoc_threshold=0.8,
                ):
                                    #TODO: implement intelligent thresholds
        self.hh = hh_key
        self.metric = metric
        self.assoc_threshold=assoc_threshold
        self.column = column
        self.support_threshold = support_threshold
        self.df = df[df['household_key'] == self.hh] # self.df is transactions for this customer only
        self.max_len = max_len
        

        # create support table upon instantiation
        
#         self.get_support_table()
     
    
    ### Support Table Function ###
    # uses fpgrowth to generate a support table
    @property
    def get_support_table(self):
        '''Return the support table for `BASKET_ID`s using `column` as product lists
        Note: 'BASKET_ID' is hardcoded...
        
        '''
        # create product lists for each basket                                   
        product_lists = self.df.groupby('BASKET_ID')[self.column].apply(list) # apply list constructor
 
        # dummy encoding...
        te = TransactionEncoder()
        te_fit = te.fit_transform(product_lists.values, sparse=True) # encode each 
        te_df = pd.DataFrame.sparse.from_spmatrix(te_fit, columns=[str(i) for i in te.columns_])
      
        # fpgrowth table
        frequent_itemsets = fpgrowth(te_df, 
                                    min_support=self.support_threshold, #can alter self.support_threshold
                                    use_colnames=True, 
#                                     verbose=True, 
                                    max_len=self.max_len,   # can alter self.max_len here.
                                    #, low_memory=True,                                   
                                    )
        # adding a length column for posterity and filtering
        frequent_itemsets['size'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
        
        # save variable for reference...
        return frequent_itemsets

    
    @property
    def assoc_table(self):
        '''change self.metric, self.assoc_threshold to rank differently'''
        ##  calling association rules on our support table
        rules = association_rules(self.support_table, metric=self.metric, min_threshold=self.assoc_threshold)
        rules["antecedent_len"] = rules["antecedents"].apply(lambda x: len(x))
        return rules
    
    def recommend(self, prev_purchases:list, howmany=5):
        '''meat and bones of the recommender system...
        accepts:
            prev_purchases: a list of previously purchased items
            howmany: (int) how many recommendations you want
            
        returns:
            a series consisting of the top 5 results given the self.metric value.
            '''
        search_terms = list(prev_purchases) # handles frozensets?
        # apply list to 'antecedent' in self.assoc_table
        search_series = pd.Series(self.assoc_table['antecedents'].apply(list)) 
        
#         print(f'Searching for {search_terms}...') # don do dat
        indexes_of_matches = []

        # for each antecedent chain...
        for item in search_terms:
            # iterate through the list of "antecedent" rows **search_series**
            for idx, val in search_series.iteritems():
                if item in val: # if the item is in the row (list of antecedents)..
                    indexes_of_matches.append(idx)

        rules = self.assoc_table.loc[indexes_of_matches]


        # RETURN TOP 5 LIFT CONSEQUENTS
        return rules.sort_values(self.metric, ascending=False)[:howmany]['consequents']