import pandas as pd
import datetime 
from utilities import read_table, query, dunnhumby_datetime_column
import sqlite3


def create_transaction_data_stage():
    '''process for src_transaction_data --> transaction_data_stg'''

    # Setup
    table_name = 'stg_transaction_data'
    col_type_mapping = {"datetime": "DATE",
                    "basket_id" :"INTEGER", 
                    "product_id": "INTEGER", 
                    "quantity": "INTEGER", 
                    "sales_value": "REAL",
                    "retail_disc": "REAL", 
                    "coupon_disc": "REAL", 
                    "coupon_match_disc": "REAL",
                    "store_id": "INTEGER",
                    "household_key": "INTEGER", 
                    # "day" :"INTEGER",
                    # "trans_time": "INTEGER", 
                    # "week_no": "INTEGER", # what does first normal form say?

                    }
    columns_string = ",".join(list(map(lambda x: f'"{x[0]}" {x[1]}', col_type_mapping.items())))
    con = sqlite3.connect('dunnhumby.db')
    con.execute(f'CREATE TABLE "{table_name}" ({columns_string})')
    
    # Extract
    transactions = read_table('src_transaction_data')

    # Transforms
    transactions['datetime'] = dunnhumby_datetime_column(transactions)
    transactions = transactions[(transactions['datetime'] >= "2004-7-1") & (transactions['datetime'] < "2006-3-1")]
    transactions.drop(['day', 'trans_time', 'week_no'], axis=1, inplace=True)
    transactions = transactions.reindex(['datetime','basket_id','product_id','quantity', 'sales_value', 'retail_disc', 'coupon_disc', 'coupon_match_disc', 'store_id','household_key'],axis=1)

    # Load 
    with con:
        try:
            columns = ",".join([f"'{x}'" for x in df.columns])
            for row in df.iterrows():
                values = ",".join([f"'{x}'" for x in row[1].values])
                #print(f'INSERT INTO {table_name} ({columns}) VALUES ({values})')
                con.execute(f'INSERT INTO {table_name} ({columns}) VALUES ({values})')
        except BaseException as e:
            print(e)
            con.rollback()

    # TEST    
    # could test column names too
    assert transactions.shape == (query(f'select count(*) from {table_name}').values[0][0], len(query(f'select * from {table_name} LIMIT 1').values[0]))
    print(f'{table_name} successfully created')