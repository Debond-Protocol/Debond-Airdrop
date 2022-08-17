import pandas as pd
import numpy as np
import math
import datetime
import time

def toTimeStamp(startDate):
    s_date = datetime.datetime.strptime(startDate, "%m/%d/%y")
    w60 = (s_date - datetime.timedelta(days=60*7)).timestamp()
    w24 = (s_date - datetime.timedelta(days=24*7)).timestamp()
    w12 = (s_date - datetime.timedelta(days=12*7)).timestamp()
    w8 = (s_date - datetime.timedelta(days=8*7)).timestamp()
    w4 = (s_date - datetime.timedelta(days=4*7)).timestamp()
    return [w60, w24, w12, w8, w4]

startDate = "8/17/18"

df_country = pd.read_csv('C:\\Users\\ralph\\Dropbox\\Debond\\classification\\countrydata.csv', encoding='ISO-8859-1')
df_data = pd.read_csv('C:\\Users\\ralph\\Dropbox\\Debond\\classification\\data5000.csv')
df_wallet = pd.read_csv("C:\\Users\\ralph\\Dropbox\\Debond\\classification\\walletdata.csv")

# FILTER ENTRIES WITH STATUS: INVALID
df_data.drop(df_data[df_data['Status'] == 'Invalid'].index, inplace=True)

# INSERT NEW BLANK COLUMNS
df_data['CountryPoint'] = np.nan
df_data['AgePoint'] = np.nan
df_data['ETHPoint'] = np.nan
df_data['ActivityPoint'] = np.nan
df_data['TotalPoint'] = np.nan

# MAKE DF WITH UNIQUE NAMES
df_data_unique = df_data.copy()
df_data_unique.drop_duplicates(subset='Name', inplace=True)
df_data_unique.reset_index(drop=True, inplace=True)

i = 0
for country, detail, dob in zip(df_data['Country'], df_data['Details'], df_data['Date of Birth']):
    if country in df_country['low-income'].values:
        df_data._set_value(i, 'CountryPoint', -1)
    elif country in df_country['lower-middle-income'].values:
        df_data._set_value(i, 'CountryPoint', 0)
    elif country in df_country['upper-middle-income'].values:
        df_data._set_value(i, 'CountryPoint', 1)
    elif country in df_country['high-income'].values:
        df_data._set_value(i, 'CountryPoint', 3)

    yr = 2022 - float(str(dob)[-4:])
    if yr < 18:
        df_data._set_value(i, 'AgePoint', 0)
    elif yr < 25:
        df_data._set_value(i, 'AgePoint', 1)
    elif yr < 40:
        df_data._set_value(i, 'AgePoint', 2)
    elif yr > 40:
        df_data._set_value(i, 'AgePoint', 3)


    # Only if detail matches to the list in wallet.csv
    if detail in df_wallet['address'].values:
        n = df_wallet[df_wallet['address'] == detail].index.values
        n = np.array(n)[0]
        eth = df_wallet['ETH'][n]

        if eth < 0.01:
            df_data._set_value(i, 'ETHPoint', -1)
        elif eth < 0.1:
            df_data._set_value(i, 'ETHPoint', 1)
        elif eth < 1:
            df_data._set_value(i, 'ETHPoint', 2)
        elif eth < 2:
            df_data._set_value(i, 'ETHPoint', 3)
        elif eth > 2:
            df_data._set_value(i, 'ETHPoint', 5)
        else:
            df_data._set_value(i, 'ETHPoint', 0)

        T = toTimeStamp((startDate))
        tx_date = df_wallet['last_TX'][n]
        if tx_date == 0:
            df_data._set_value(i, 'ActivityPoint', 0)
        elif tx_date < T[0]:
            df_data._set_value(i, 'ActivityPoint', -3)
        elif tx_date < T[1]:
            df_data._set_value(i, 'ActivityPoint', -1)
        elif tx_date < T[2]:
            df_data._set_value(i, 'ActivityPoint', 1)
        elif tx_date < T[3]:
            df_data._set_value(i, 'ActivityPoint', 2)
        elif tx_date > T[4]:
            df_data._set_value(i, 'ActivityPoint', 3)
        else:
            df_data._set_value(i, 'ActivityPoint', 0)

        print(detail)
        print(f'ETH: {eth}, ETH point: {df_data["""ETHPoint"""][i]}')
        print(f'Activity point: {df_data["""ActivityPoint"""][i]}')
        print()
    i += 1

i = 0
for name in df_data_unique['Name']:
    country_sum = df_data.loc[df_data['Name'] == name].CountryPoint.sum()
    age_sum = df_data.loc[df_data['Name'] == name].AgePoint.sum()
    eth_sum = df_data.loc[df_data['Name'] == name].ETHPoint.sum()
    activity_sum = df_data.loc[df_data['Name'] == name].ActivityPoint.sum()

    total_point = country_sum + age_sum + eth_sum + activity_sum

    print(f'Name: {name}, Eth: {eth_sum}, act: {activity_sum}')

    df_data_unique._set_value(i, 'CountryPoint', country_sum)
    df_data_unique._set_value(i, 'AgePoint', age_sum)
    df_data_unique._set_value(i, 'ETHPoint', eth_sum)
    df_data_unique._set_value(i, 'ActivityPoint', activity_sum)
    df_data_unique._set_value(i, 'TotalPoint', total_point)
    i += 1

df_data_unique = df_data_unique.sort_values(['TotalPoint'], ascending=False)
# df_data_unique.to_excel('out2.xlsx')
print(df_data_unique)
