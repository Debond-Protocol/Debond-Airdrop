from urllib.request import Request, urlopen
import pandas as pd
import json

#Load CSV
df= pd.read_csv ('gleam_wallet.csv')
df=df.tail(1000000)

pd.set_option('display.max_columns',None)
pd.set_option('display.max_row',None)

Wallet_address=df['Details'].values.tolist()
country=df['Country'].values.tolist()
date_birth=df['Date of Birth'].values.tolist()

print(Wallet_address)
#scraper seeting
#header=Headers(browser='firefox',os="Linux",headers=True)
#print(header.generate())
ethplorer_api=["EK-mPZkt-jzXUNw3-hYUwu"]
print(ethplorer_api)


def verifier(start,end,df,ethplorer_api):

    TX_hash=[]
    TX_input_to_decode=[]
    api_key_index=1

    Verified_address=[]
    Verified_country = []
    Verified_birth = []


    Verified_TX=[]
    Verified_ETH=[]
    Verified_last_TX = []

    if end >= len(Wallet_address)-1:
        end == len(Wallet_address)-1
    loop_times=(end-start)

    for i in range(loop_times):
         try:

            #setting api_key
            api_key= ethplorer_api[api_key_index % len(ethplorer_api) -1]

            i+=start

            print("=======" + str(i) + "=======")
            #get the tx history
            #print('https://api.ethplorer.io/getAddressTransactions/'+Wallet_address[i]+'?apiKey='+api_key)
            req = Request('https://api.ethplorer.io/getAddressTransactions/'+Wallet_address[i]+'?apiKey='+api_key,
                                  headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            my_json = webpage.decode('utf8')
            s1 = json.loads(my_json)

            print(Wallet_address[i]+"TXs="+str(len(s1)))

            #get the ETH balance
            #print('https://api.ethplorer.io/getAddressInfo/'+Wallet_address[i]+'?apiKey='+api_key)
            req = Request(
                'https://api.ethplorer.io/getAddressInfo/'+Wallet_address[i]+'?apiKey=' + api_key,
                headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()

            my_json = webpage.decode('utf8')

            s2 = json.loads(my_json)
            print(Wallet_address[i]+"  ETH="+str(s2["ETH"]["balance"]))

            Verified_TX.append(len(s1))

            if len(s1) == 0:
                Verified_last_TX.append( 0 )
            else:
                Verified_last_TX.append(s1[len(s1)-1]["timestamp"])


            Verified_address.append(Wallet_address[i])
            Verified_country.append(country[i])
            Verified_birth.append(date_birth[i])

            Verified_ETH.append(s2["ETH"]["balance"])

            #index
            api_key_index+=1

            #print(Wallet_address[i]+","+Verified_country[i]+","+str(Verified_birth[i])+","+str(Verified_ETH[i])+","+str(Verified_TX[i])+","+str(Verified_last_TX[i]))
         except:
             print("error!")
             Verified_address.append("NaN")
             Verified_country.append("NaN")
             Verified_birth.append(0)

             Verified_TX.append(0)
             Verified_ETH.append(0)
             Verified_last_TX.append(0)

    return(Verified_address,Verified_country,Verified_birth,Verified_ETH,Verified_TX,Verified_last_TX)

start_at=20001
end_at=33196

DATA=verifier(start_at,end_at,df,ethplorer_api)
print(DATA)
df2 = pd.DataFrame(columns=['address',"country",'birth','ETH','TX','last_TX'])
df2["address"]=DATA[0]
print(DATA[0])
df2["country"]=DATA[1]
print(DATA[1])
df2["birth"]=DATA[2]
print(DATA[2])

df2["ETH"]=DATA[3]
df2["TX"]=DATA[4]
df2["last_TX"]=DATA[5]

print(df2)
name='Gleam'+str(start_at)+'_to_'+str(end_at)+'.csv'
print(name)
df2.to_csv(name)