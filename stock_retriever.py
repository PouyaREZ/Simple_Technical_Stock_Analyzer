# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 21:39:05 2018

Stocks retriever: obtains 3yr, 1yr, 3m, and 1m ROIs for the list of Indices,
                  and stores them in Stock_Updated.xlsm

@Author: Pouya Rezazadeh Kalehbasti (Rezazadeh.Pouya@gmail.com)
"""


from iexfinance import get_historical_data as ghd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pandas.tseries.offsets import BDay
import pandas as pd
from numpy import average
# from scoop import futures

Measures = {} # dictionary of [1m, 3m, 1y, 5y] ROIs

# Indices = ['AMD', 'NVDA', 'AAPL', 'FIVN', 'SQ', 'SPY', 'HQY', 'SODA',
           # 'NOVT', 'SPXL', 'BA', 'SPHD','LMT','ADBE',
           # 'MED', 'QLD', 'INTC', 'SFIX', 'HRS',
           # 'WIX', 'AMZN', 'NFLX', 'GOOGL', 'TEAM', 'SPGI', 'DIA',
           # 'QQQ', 'SNE', 'TECH', 'INGN', 'NKE', 'EA', 'ATVI', 'VOO',
           # 'IVV', 'IVW','JNK','HYG', 'MSFT', 'TM', 'HMC', 'CAT', 'JPM',
           # 'TMUS', 'VZ', 'T','FB','SOCL','BRK.B', 'PFE', 'AXP','HD',
           # 'UTX','V','MRK', 'CSCO','UNH', 'ETN', 'AOS', 'CTAS', 'MU',
           # 'KO', 'GM','CRM','AMRN','SNAP']
Indices = ['VTI','SPY','IEFA','IVV','VOO','EFA','VEA','VWO','QQQ','AGG', 'SPXL', 'XBI','DIA','IJH','IJR','XLI','XLK','HDV','XLV','IHI','VHT'] 
non_normalized = True

Portfolio_Value = 2880 #$






## Date definitions
end = datetime.now()
start = end - relativedelta(years=1) - 3*BDay()

Six_M_Date_Full = end - relativedelta(months=6) - 2*BDay()
Six_M_Date = Six_M_Date_Full.strftime('%Y-%m-%d')

Three_M_Date_Full = end - relativedelta(months=3) - BDay()
Three_M_Date = Three_M_Date_Full.strftime('%Y-%m-%d')

One_M_Date_Full = end - relativedelta(months=1) - BDay()
One_M_Date = One_M_Date_Full.strftime('%Y-%m-%d')

One_W_Date_Full = end - relativedelta(weeks=1) - BDay()
One_W_Date = One_W_Date_Full.strftime('%Y-%m-%d')

## Main function: retrieve the data and find the desired measures
if __name__ == '__main__':
    # data_frames = list(futures.map(lambda x: ghd(x, start = start, end = end, output_format = 'pandas'), Indices))
    data_frames = ghd(Indices, start = start, end = end, output_format = 'pandas')
    # for i in range(len(Indices)):
    for ind in Indices:
        df = data_frames[ind]
        Price = df['close'][-1] # Today's closing price
        One_Yr = (Price-df['open'][0])/df['open'][0] # 3Yr ROI
        Six_Mn = (Price-df['open'][Six_M_Date])/df['open'][Six_M_Date]
        Three_Mn = (Price-df['open'][Three_M_Date])/df['open'][Three_M_Date]
        One_Mn = (Price-df['open'][One_M_Date])/df['open'][One_M_Date]
        One_Wk = (Price-df['open'][One_W_Date])/df['open'][One_W_Date]
        Volat = average(df['close'].rolling(window = 10).std(ddof = 0)[-1:-11:-1])
        
        Measures[ind] = [One_Yr, Six_Mn, Three_Mn, One_Mn, One_Wk, Price, Volat]
    
    if not(non_normalized):
        Max_1_Yr = max([x[0] for x in Measures.values()])
        Max_6_M = max([x[1] for x in Measures.values()])
        Max_3_M = max([x[2] for x in Measures.values()])
        Max_1_M = max([x[3] for x in Measures.values()])
        Max_1_W = max([x[4] for x in Measures.values()])
        ## Calculating scores and storing in the dict
        for ind in Measures.keys(): # Coeffs: 1 for 3yr, 1.5 for 1 yr, 2 for <1yr
            Score = (1*Measures[ind][0]/Max_1_Yr + 1.5*Measures[ind][1]/Max_6_M 
                     + 2.0*Measures[ind][2]/Max_3_M + 2.5*Measures[ind][3]/Max_1_M
                     + 3.0*Measures[ind][4]/Max_1_W)  
            Measures[ind][6] /= Measures[ind][5] # Normalizing volatility based on price
            Measures[ind].append(Score)
    else:
        for ind in Measures.keys(): # Coeffs: 1 for 3yr, 1.5 for 1 yr, 2 for <1yr
            Score = (1*Measures[ind][0] + 1.5*Measures[ind][1] 
                     + 1.75*Measures[ind][2] + 2*Measures[ind][3]
                     + 2.25*Measures[ind][4])  
            Measures[ind][6] /= Measures[ind][5] # Normalizing volatility based on price
            Measures[ind].append(Score)
    
    
    
    
    ## Sorting the dictionary
    Measures = dict(sorted(Measures.items(), key = lambda x: x[1][7], reverse = True))


    df_to_save = pd.DataFrame(data = Measures, index = ['1yr','6m','3m','1m','1w','Price','Volat','Score'])
    df_to_save.to_excel('Stock_Updated.xlsx')
    # df_to_save.to_excel('Stock_Updated_Test.xlsx')