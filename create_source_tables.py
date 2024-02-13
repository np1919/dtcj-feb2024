import pandas as pd
import sqlite3
from utilities import query, drop_table, read_table

def create_section_labels_table():
    '''section labels.txt was manually parsed from all sub_commodity_descriptions.'''
    with open('Section_Labels.txt') as f:
        data = f.readlines()
    data = eval(data[0]) # hardcoding an eval line isn't necessarily best practices..?
    con = con = sqlite3.connect('dunnhumby.db')
    with con:
        try:
            con.execute('CREATE TABLE IF NOT EXISTS section_labels ("commodity_desc" TEXT PRIMARY KEY, "section_label" TEXT)')
            for k,v in data.items():
                con.execute(f'INSERT INTO section_labels ("commodity_desc", "section_label") VALUES ("{k}", "{v}")')
        except BaseException as e:
            print(e)
            con.rollback()
    # TEST
    assert len(read_table('section_labels')) == len(data)


def create_product_source():
    table_name = 'src_product'
    con = sqlite3.connect('dunnhumby.db')
    with con:
        try:
            df = pd.read_csv('data/product.csv')
            columns = ",".join([f"'{x}'" for x in df.columns])
            con.execute(f'CREATE TABLE "{table_name}" (product_id INTEGER PRIMARY KEY, manufacturer INTEGER, department TEXT, brand TEXT, commodity_desc TEXT, sub_commodity_desc TEXT, curr_size_of_product TEXT)')
            # could use any iterable or data stream
            for row in df.iterrows():
                values = ",".join([f"'{x}'" for x in row[1].values])
                #print(f'INSERT INTO {table_name} ({columns}) VALUES ({values})')
                con.execute(f'INSERT INTO {table_name} ({columns}) VALUES ({values})')
        except BaseException as e:
            print(e)
            con.rollback()
    # TEST    
    # could test column names too
    assert df.shape == (query(f'select count(*) from {table_name}').values[0][0], len(query(f'select * from {table_name} LIMIT 1').values[0]))
    print(f'{table_name} successfully created')


def create_transaction_data_source():
    ''' no primary key defined here... should be compound betweeen basket_id and product_id if im not mistaken.. '''
    table_name = 'src_transaction_data'
    col_type_mapping = {"household_key": "INTEGER", 
                        "basket_id" :"INTEGER", 
                        "day" :"INTEGER", "product_id": 
                        "INTEGER", "quantity": "INTEGER", 
                        "sales_value": "REAL", "store_id": 
                        "INTEGER", "retail_disc": "REAL", 
                        "trans_time": "INTEGER", "week_no": 
                        "INTEGER", "coupon_disc": "REAL", 
                        "coupon_match_disc": "REAL"}
    columns_string = ",".join(list(map(lambda x: f'"{x[0]}" {x[1]}', col_type_mapping.items())))

    con = sqlite3.connect('dunnhumby.db')
    con.execute(f'CREATE TABLE "{table_name}" ({columns_string})')
    with con:
        try:
            df = pd.read_csv('data/transaction_data.csv')
            columns = ",".join([f"'{x}'" for x in df.columns])
            # could use any iterable or data stream
            for row in df.iterrows():
                values = ",".join([f"'{x}'" for x in row[1].values])
                #print(f'INSERT INTO {table_name} ({columns}) VALUES ({values})')
                con.execute(f'INSERT INTO {table_name} ({columns}) VALUES ({values})')
        except BaseException as e:
            print(e)
            con.rollback()
    # TEST    
    # could test column names too
    assert df.shape == (query(f'select count(*) from {table_name}').values[0][0], len(query(f'select * from {table_name} LIMIT 1').values[0]))
    print(f'{table_name} successfully created')


def create_hh_demographic_source():
    name = 'hh_demographic'
    table_name = f'src_{name}'
    con = sqlite3.connect('dunnhumby.db')
    with con:
        try:
            df = pd.read_csv(f'{data_folder}{name}.csv')
            columns = ",".join([f"'{x}'" for x in df.columns])
            con.execute(f'CREATE TABLE "{table_name}" (age_desc TEXT, marital_status_code TEXT, income_desc TEXT, homeowner_desc TEXT, hh_comp_desc TEXT, household_size_desc TEXT, kid_category_desc TEXT, household_key INTEGER PRIMARY KEY)')
            # could use any iterable or data stream
            for row in df.iterrows():
                values = ",".join([f"'{x}'" for x in row[1].values])
                #print(f'INSERT INTO {table_name} ({columns}) VALUES ({values})')
                con.execute(f'INSERT INTO {table_name} ({columns}) VALUES ({values})')
        except BaseException as e:
            print(e)
            con.rollback()
    # TEST    
    # could test column names too
    assert df.shape == (query(f'select count(*) from {table_name}').values[0][0], len(query(f'select * from {table_name} LIMIT 1').values[0]))
    print(f'{table_name} successfully created')