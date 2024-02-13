import sqlite3
import pandas as pd
import datetime as dt


def query(query, db='dunnhumby.db'):
    con = sqlite3.connect(db)
    with con:
        res = con.execute(" ".join([x.strip('\n').strip('\t').strip(' ') for x in query.split()]))
        colnames = [x[0] for x in res.description]
        output = pd.DataFrame(res.fetchall(), columns=colnames)
    # con.close()
    return output


def list_all_tables(db='dunnhumby.db'):
    con = sqlite3.connect(db)
    with con:
        res = con.execute("SELECT name FROM sqlite_master WHERE type='table';")
    output = list(res.fetchall())
    con.close()
    return [x[0] for x in output]


def drop_table(table_name:str, db='dunnhumby.db'):
    con = sqlite3.connect(db)
    # drop the table
    with con:
        con.execute(f"DROP TABLE '{table_name}';")
        print(f'dropped table {table_name}')


# read the table
def read_table(from_clause:str,
                select_clause:str = "SELECT *",
                where_clause:str='',
                group_by:str="",
                order_by:str="",
                db='dunnhumby.db'):
    '''spaces between clauses already exist'''

    con = sqlite3.connect(db)
    with con:
        res = con.execute(f'{select_clause} FROM {from_clause} {where_clause} {group_by} {order_by}')
        colnames = [x[0] for x in res.description]
    
    return pd.DataFrame(res.fetchall(), columns=colnames)#.set_index('date')


def datetime_to_date(df, datetime_col='datetime',return_date_col:bool=True, return_week_number:bool=False ):
    output = []
    df[datetime_col] = pd.to_datetime(df[datetime_col])
    if return_date_col == True:
        output.append(df[datetime_col].dt.date)
    if return_week_number == True:
        output.append(df[datetime_col].dt.isocalendar().week)
        # merged["Week"] = 
        # df[datetime_col].dt.to_period("W").dt.to_timestamp()
        # df[datetime_col].dt.isocalendar().week
    return output


def dunnhumby_datetime_column(df, date_col='day', time_col='trans_time'):

    def make_date_map(df, dates=date_col):
        # 'DAY' 1 == 2004-03-23
        day1 = dt.datetime(2004, 3, 23) # as derived in transactions notebook; datetime for 'DAY' == 1
        ineedthismany = df[dates].max()
        last = day1 + dt.timedelta(days=int(ineedthismany))
        date_range = pd.date_range(day1, last) # date range for our data
        # map datetime index to DAY; enumerate() indexes from 0, so we add 1
        date_map = {i+1:x for i, x in enumerate(date_range)}

        output = df[dates].map(date_map)
        output = pd.to_datetime(output)
        return output

    def make_time_map(df, times=time_col):
        ''''''
        # pad zeros
        output = df[times].astype(str).str.zfill(4)

        # split to hours and minutes
        hours = output.str[:2]
        minutes = output.str[2:]

        # convert to timedelta
        hours = pd.to_timedelta(hours.astype('int'), unit='hour')
        minutes = pd.to_timedelta(minutes.astype('int'), unit='minute')
        output = hours + minutes
        return output
    return make_date_map(df) + make_time_map(df)