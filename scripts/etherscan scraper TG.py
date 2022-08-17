from urllib.request import Request, urlopen
import pandas as pd
import json

#Load CSV
df= pd.read_csv ('airdrop_bot.csv')
df=df.tail(1000000)

pd.set_option('display.max_columns',None)
pd.set_option('display.max_row',None)
Wallet_address=df['Wallet'].values.tolist()
Ref=df['Invited'].values.tolist()



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
    Verified_ref=[]

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
            Verified_TX.append(len(s1))
            print(Wallet_address[i]+"TXs="+str(len(s1)))
            if len(s1) == 0:
                Verified_last_TX.append( 0 )
            else:
                Verified_last_TX.append(s1[len(s1)-1]["timestamp"])


            #get the ETH balance
            #print('https://api.ethplorer.io/getAddressInfo/'+Wallet_address[i]+'?apiKey='+api_key)
            req = Request(
                'https://api.ethplorer.io/getAddressInfo/'+Wallet_address[i]+'?apiKey=' + api_key,
                headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()

            my_json = webpage.decode('utf8')

            s2 = json.loads(my_json)
            print(Wallet_address[i]+"  ETH="+str(s2["ETH"]["balance"]))

            Verified_address.append(Wallet_address[i])
            Verified_ref.append(Ref[i])

            Verified_ETH.append(s2["ETH"]["balance"])

            #index
            api_key_index+=1
            #print(Wallet_address[i]+","+str(Verified_ETH[i])+","+str(Verified_TX[i])+","+str(Verified_last_TX[i]))
         except:
             print("error")

             Verified_address.append("NaN")
             Verified_ref.append(0)


             Verified_TX.append(0)
             Verified_ETH.append(0)
             Verified_last_TX.append(0)
             pass
    return(Verified_address,Verified_ETH,Verified_TX,Verified_last_TX,Verified_ref)


start_at=16001
end_at=32070

DATA=verifier(start_at,end_at,df,ethplorer_api)

df2 = pd.DataFrame(columns=['address','ETH','TX','last_TX','ref'])
df2["address"]=DATA[0]
df2["ETH"]=DATA[1]
df2["TX"]=DATA[2]
df2["last_TX"]=DATA[3]
df2["ref"]=DATA[4]




name='TG_airdrop'+str(start_at)+'to'+str(end_at)+'.csv'
print(name)
df2.to_csv(name)