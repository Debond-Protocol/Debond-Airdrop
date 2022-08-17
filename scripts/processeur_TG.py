import pandas as pd
import datetime


df_country = pd.read_csv('Book1.csv')
name='TG_airdrop16001_to_32070.csv'
df = pd.read_csv(name)
df=df.tail(1000000)

print(df)
def toTimeStamp(startDate):
    s_date = datetime.datetime.strptime(startDate, "%m/%d/%y")
    w60 = (s_date - datetime.timedelta(days=60*7)).timestamp()
    w24 = (s_date - datetime.timedelta(days=24*7)).timestamp()
    w12 = (s_date - datetime.timedelta(days=12*7)).timestamp()
    w8 = (s_date - datetime.timedelta(days=8*7)).timestamp()
    w4 = (s_date - datetime.timedelta(days=4*7)).timestamp()
    return [w60, w24, w12, w8, w4]

startDate = "8/17/18"


address=df['address'].values.tolist()
tx=df['TX'].values.tolist()
eth=df['ETH'].values.tolist()
last_TX=df['last_TX'].values.tolist()



i = 0
def pointer():

    for i in range(len(address)-1):

        print(eth[i] )
        if eth[i] < 0.01:
            df._set_value(i, 'ETHPoint', -1)
        elif eth[i]  < 0.1:
            df._set_value(i, 'ETHPoint', 1)
        elif eth[i]  < 0.5:
            df._set_value(i, 'ETHPoint', 2)
        elif eth[i] < 1:
            df._set_value(i, 'ETHPoint', 2)
        elif eth[i]  < 2:
            df._set_value(i, 'ETHPoint', 4)
        elif eth[i]  >= 2:
            df._set_value(i, 'ETHPoint', 5)
        elif eth[i]  >= 10:
            df._set_value(i, 'ETHPoint', 10)
        else:
            print("error!")
            df._set_value(i, 'ETHPoint', 0)

        print(last_TX[i])
        T = toTimeStamp((startDate))
        if last_TX[i] == 0:
            df._set_value(i, 'ActivityPoint', -1)
        elif 0 < last_TX[i] < T[0]:
            df._set_value(i, 'ActivityPoint', 0)
        elif last_TX[i] < T[1]:
            df._set_value(i, 'ActivityPoint', 1)
        elif last_TX[i] < T[2]:
            df._set_value(i, 'ActivityPoint', 2)
        elif last_TX[i] < T[3]:
            df._set_value(i, 'ActivityPoint', 3)
        elif last_TX[i] >= T[4]:
            df._set_value(i, 'ActivityPoint', 4)
        else:
            print("error!")
            df._set_value(i, 'ActivityPoint', -1)

        sum_point=df['ETHPoint'][i]+df['ActivityPoint'][i]
        df._set_value(i, 'TotalPoint', sum_point)
    return(df)


DATA=pointer()


print(DATA)
prefix='processed_'
print(prefix+name)
DATA.to_csv(prefix+name)