import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt


def load_campaign_summary(merged):
    
    campaign_desc = pd.read_csv('data/campaign_desc.csv')
    coupon = pd.read_csv('data/coupon.csv')

    def campaign_products():

        #### CONTAINER
        results = dict()

        for camp_no in range(1,31):
            #### RUSSIAN DOLL
            results[camp_no] = dict()


            #### FIRST AND LAST DAY
            first, last = list(campaign_desc[campaign_desc['CAMPAIGN'] == camp_no][['START_DAY', 'END_DAY']].iloc[0, :].values)
            # boundary assertions for first, last
            if first < merged['DAY'].min():
                first = merged['DAY'].min()
            if last > 711: # campaign 24 has an erroneous LAST_DAY
                last = 711
            # store first/last
            results[camp_no]['First Day'] = first
            results[camp_no]['Last Day'] = last

            #### TOTAL DURATION
            results[camp_no]['Duration'] = (last - first) +1



            #### PRODUCT LISTS
            results[camp_no]['Listed Products'] = coupon_list = list(coupon[coupon['CAMPAIGN'] == camp_no]['PRODUCT_ID'])
            #### SECTION LABELS 
            results[camp_no]['Section Label Counts'] = {v:k for (k, v) in zip(merged[merged['PRODUCT_ID'].isin(coupon_list)]['Section Labels'].value_counts(), merged[merged['PRODUCT_ID'].isin(coupon_list)]['Section Labels'].value_counts().index)}

            # Overall
            results[camp_no]['Listed Products Total Sales'] = merged[merged['PRODUCT_ID'].isin(coupon_list)]['SALES_VALUE'].sum()
            # avg. sales before the campaign
            results[camp_no]['Listed Products Sales Before'] = merged[merged['PRODUCT_ID'].isin(coupon_list) & (merged['DAY'] < first)]['SALES_VALUE'].sum()

            # avg. daily sales of mergeds in the campaign 
            # During the campaign 
            results[camp_no]['Listed Products Sales During'] = merged[(merged['PRODUCT_ID'].isin(coupon_list)) & (merged['DAY'].isin(range(first, last + 1)))]['SALES_VALUE'].sum()

            results[camp_no]['Listed Products Sales After'] = merged[(merged['PRODUCT_ID'].isin(coupon_list)) & (merged['DAY'] > last)]['SALES_VALUE'].sum()


        return results

    def campaign_sales():
        df = pd.DataFrame()
        product_lists = dict()

        for camp_no in range(1, 31):
        #     camp_no = 1
            first, last = list(campaign_desc[campaign_desc['CAMPAIGN'] == camp_no][['START_DAY', 'END_DAY']].iloc[0, :].values)
            coupon_list = list(coupon[coupon['CAMPAIGN'] == camp_no]['PRODUCT_ID'])
            product_lists[camp_no] = coupon_list

            # Assertion for day limits
            if first < merged['DAY'].min():
                first = merged['DAY'].min()
            if last > 711: # campaign 24 has an erroneous LAST_DAY
                last = 711

            # avg. daily sales of products in the campaign, overall
            total = merged[merged['PRODUCT_ID'].isin(coupon_list)]['SALES_VALUE'].sum() / (712 - merged['DAY'].min())

            # avg. daily sales of products in the campaign, before the campaign
            before = merged[merged['PRODUCT_ID'].isin(coupon_list) & (merged['DAY'] < first)]['SALES_VALUE'].sum() / (first+1 - merged['DAY'].min())

            # avg. daily sales of products in the campaign , during the campaign
            during = merged[(merged['PRODUCT_ID'].isin(coupon_list)) & (merged['DAY'].isin(range(first, last + 1)))]['SALES_VALUE'].sum() / (last+1 - first)

            # avg daily sales of products in the campaign, after the campaign
            after = merged[(merged['PRODUCT_ID'].isin(coupon_list)) & (merged['DAY'] > last)]['SALES_VALUE'].sum() / (712-last)

            df = df.append(pd.Series([total, before, during, after, first, last]), ignore_index=True)

        # add index (campaign) and columns
        df.columns = ['avg. total', 'avg. before', 'avg. during', 'avg. after', 'first', 'last']
        df.index = (range(1,31))
        return df

    return pd.DataFrame(campaign_products()).T.join(campaign_sales())
    
    ## TODO: add totals?
