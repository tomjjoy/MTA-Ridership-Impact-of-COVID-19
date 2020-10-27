
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyspark as ps
import scipy.stats as stats
from uszipcode import SearchEngine


plt.style.use('ggplot')




def get_zip_income():
    '''Gets all median incomes per zip code in NYC via uszipcode'''
    
    search = SearchEngine(simple_zipcode=True) # set simple_zipcode=False to use rich info database
    zipcode = search.by_zipcode("10001")
    zipcode

    data_by_zip = pd.read_csv('../data/data-by-modzcta.csv')
    zip_lst = data_by_zip['MODIFIED_ZCTA']

    # zipcode.values() # to list
    zipcode_lst = list(zip_lst)
    median_income = []
    for i in zipcode_lst:
        zc = search.by_zipcode(i)
        median_income.append((i, zc.to_dict()['median_household_income'])) # to dict
    
    
    return pd.DataFrame(median_income, columns=['zip', 'median_income'])


def get_covid_data():
    '''Retreaves All COVID-19 Data via CSV's '''
    
    data_by_zip = pd.read_csv('../data/data-by-modzcta.csv')
    tests_by_day = pd.read_csv('../data/tests.csv')
    tests_by_boro = pd.read_csv('../data/by-boro.csv')
    
    return data_by_zip, tests_by_day, tests_by_boro


def fixing_datetime(df):
    '''Converts DataFrame Date Column to DateTime Format'''
    
    df['Date'] = pd.to_datetime(df.Date)
    if (df.Date == pd.Timestamp("2020-04-01")).any():
        start_date_2020 = '2020-03-01'
        end_date_2020 = '2020-09-30'
        date_range = (df['Date'] >= start_date_2020) & (df['Date'] <= end_date_2020)
        df_2020 = df.loc[date_range]
        return df_2020
        
    elif (df.Date == pd.Timestamp("2019-04-01")).any():
        start_date = '2019-03-01'
        end_date = '2019-09-30'
        date_range = (df['Date'] >= start_date) & (df['Date'] <= end_date)
        df_2019 = df.loc[date_range]
        return df_2019
    
    else:
        return df