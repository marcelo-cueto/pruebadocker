#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


from binance.client import Client
import json
from datetime import datetime


# In[2]:


import plotly.graph_objects as go
from plotly.subplots import make_subplots as splt
import math
import time
import numpy as np
import pandas as pd
import datetime as dt
from pylab import plt, mpl


# In[3]:


apiKey = "A9biVu4c9VJwpMSNmDWzEk9qnN53YzsD0lPaHHvUSyGAZZpsuLbEBvXc2fn4Q8lI"
secret = '3wmdWG22JSBy4Nl5tDyATOZGPRv8YnPj9JqW2B05yO5eUophdxqMZNEgvqr7exxf'
client = Client(apiKey, secret,tld='com')


# In[4]:


import time


# In[5]:


import nest_asyncio
import asyncio
nest_asyncio.apply()
from binance import AsyncClient, BinanceSocketManager


# In[6]:


from ta.momentum import rsi #RSI


# In[7]:


import ta


# In[8]:


import nest_asyncio
import asyncio
nest_asyncio.apply()
from binance import AsyncClient, BinanceSocketManager


# In[9]:



units =float(client.get_asset_balance('BUSD')['free'])
asset=float(client.get_asset_balance('DOGE')['free'] )       
if  units > asset:
    position = -1
else:
    position = 1
bar = '5m'  

klines = client.get_historical_klines('DOGEBUSD', Client.KLINE_INTERVAL_5MINUTE, '2 days ago')
timet=[]
high=[]
low=[]
closep=[]
open=[]
volume=[]
marcador=0
contador=-1
for a in klines:
    contador+=1
    ac=a[0]/1000
    b=datetime.utcfromtimestamp(ac).strftime('%Y-%m-%d %H:%M:%S')
    timet.append(b)
    high.append(float(a[2]))
    low.append(float(a[3]))
    closep.append(float(a[4]))
    volume.append(float(a[5]))
    if marcador == 0:
        open.append(float(a[3]))
        marcador=1
    else:
        open.append(float(klines[contador-1][4]))
    
    
df = pd.DataFrame({'Date': timet, 'High': high, 'Low': low, 'Close': closep, "Open": open, 'Volume': volume, 'balance USD':0, 'unidades EOS':0 })


            


# In[10]:


import pymannkendall as pmk




# In[12]:


import os
uno=os.path.exists('doge.csv')


# In[13]:


if uno == False:
    trades=pd.DataFrame()
else:
    trades=pd.read_csv('doge.csv')


# In[ ]:


async def main():
    client = await AsyncClient.create(apiKey, secret)
    bm = BinanceSocketManager(client)
    # start any sockets here, i.e a trade socket
    ts = bm.kline_socket('DOGEBUSD',interval='5m')
    # then start receiving messages
    async with ts as tscm:
        while True:
            res = await tscm.recv()
            global df
            global trades
            global position
            global asset
            global units
            comin=78
            venin=41
            vende=22
            comde=49
            venno=43
            comno=74
            venmin=20
            commin=50
            venmax=45
            commax=87
            
            if res['k']['x']== True:
                print(res['k']['c'])
                ac=res['k']['t']/1000
                b=datetime.utcfromtimestamp(ac).strftime('%Y-%m-%d %H:%M:%S')
                high=float(res['k']['h'])
                low=float(res['k']['l'])
                closep=float(res['k']['c'],)
                volume=float(res['k']['v'])
               
                df= df.append({'Date': b, 'High': high, 'Low': low, 'Close': closep, "Open": res['k']['o'], 'Volume': volume, 'balance USD':0, 'unidades EOS':0 },ignore_index=True) 
                df = df.iloc[-289 : ]
                df_aux=df
                
                df_aux['Date']=pd.to_datetime(df_aux['Date'], dayfirst=True)
                df_aux.dropna(inplace=True)       
                df_aux = df_aux.set_index('Date') 
                df_aux['posicion'] = 0 # creo columna posicion con valor 0
                df_aux['unix']=df_aux.index.astype(np.int64) // 10 ** 9   
                from scipy.signal import argrelextrema
                from ta.momentum import rsi 
                
                df_aux['RSI'] = rsi(df_aux['Close'].astype(float), 14, False)
                 
                mk=pmk.original_test(df_aux['Close'][60:], alpha=0.05)


                if mk.z < -1 and mk.z>=-16:
                    sobrevendido=vende
                    sobrecomprado=comde
                elif mk.z > 1 and mk.z<=16:
                    sobrevendido=venin
                    sobrecomprado=comin
                elif mk.z >= -1 and mk.z<=1: 
                    sobrevendido=venno
                    sobrecomprado=comno
                elif mk.z>16:
                    sobrevendido=venmax
                    sobrecomprado=commax
                else:
                    sobrevendido=venmin
                    sobrecomprado=commin
                    
                soportes = df_aux['Close'].iloc[argrelextrema(df_aux['Close'].values, np.less_equal, order=3)]
                
                resistencias = df_aux['Close'].iloc[argrelextrema(df_aux['Close'].values, np.greater_equal, order=3)]
                min= df_aux['Close'].min()
                max= df_aux['Close'].max()
                sop2=(soportes[-2]-min)/(max-min)
                sop1=(soportes[-1]-min)/(max-min)
                res2=(resistencias[-2]-min)/(max-min)
                res1=(resistencias[-1]-min)/(max-min)
                soportes_y=((df_aux['unix'][soportes.index[-2]]/60/5 )- (df_aux['unix'][soportes.index[-1]]/60/5)) / ((sop2 - sop1)*10)
                rsi_sop_y=((df_aux['unix'][soportes.index[-2]]/60/5 )- (df_aux['unix'][soportes.index[-1]]/60/5)) / (df_aux['RSI'][soportes.index[-2]] - df_aux['RSI'][soportes.index[-1]])

                resistencias_y=((df_aux['unix'][resistencias.index[-2]]/60/5 )- (df_aux['unix'][resistencias.index[-1]]/60/5)) / ((res2 - res1)*10)
                rsi_res_y=((df_aux['unix'][resistencias.index[-2]]/60/5 )- (df_aux['unix'][resistencias.index[-1]]/60/5)) / (df_aux['RSI'][resistencias.index[-2]] - df_aux['RSI'][resistencias.index[-1]])
                print(math.floor(units/float(res['k']['c'])))
                if df_aux['RSI'].iloc[-1] < 40:
                    print("entro rsi")
                    if (resistencias_y*0.3) < rsi_res_y:
                        print("entro diver")
                        if position in [0, -1]: # Compurba si la posicion es nula o short
                            print('*** GOING LONG ***')
                           
                            
                            res=await client.create_order(symbol='DOGEBUSD', side='BUY', type='MARKET',quantity=math.floor((units/float(res['k']['c'])-1)),newOrderRespType='RESULT' ) 
                            time.sleep(1)
                            val=await client.get_asset_balance('DOGE')
                            time.sleep(1)
                            valu=await client.get_asset_balance('BUSD')
                            time.sleep(1)
                            asset=float(val['free'])
                            units=float(valu['free'])
                           
                            trades.to_csv('trades.csv', sep=',')
                            print('#'*150)
                            print('Se compra  {} DOGE a {}  usd a las{}  |'.format(res['executedQty'], res['price'], res['transactTime']))     
                            print('#'*150) 
                            position = 1
                      

                  # Señal para ir Short
                if df_aux['RSI'].iloc[-1] > 69:
                      if float((soportes_y*0.3)) >rsi_sop_y:
                            if position in [1]:
                                print('*** GOING SHORT ***')
                                
                                res= await client.create_order(symbol='DOGEBUSD', side='SELL', type='MARKET', quantity=math.floor(asset), newOrderRespType='RESULT' ) 
                                time.sleep(1)
                                val= await client.get_asset_balance('DOGE')
                                time.sleep(1)
                                valu=await client.get_asset_balance('BUSD')
                                time.sleep(1)
                                
                                asset=float(val['free'])
                                units=float(valu['free'])
                               
                                trades.to_csv('trades.csv', sep=',')
                                print('#'*150)
                                print('Se vende  {} DOGE a {}  usd a las{}  |'.format(res['executedQty'], res['price'], res['transactTime']))     
                                print('#'*150)        
                                position = -1

                      
                
    await client.close_connection()

if __name__ == "__main__":

    loop = asyncio.get_event_loop() 
    loop.run_until_complete(main())


# In[ ]:


df.tail()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




