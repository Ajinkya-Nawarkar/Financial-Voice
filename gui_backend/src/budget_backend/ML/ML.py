#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 22:47:54 2018

@author: meenakshidas
"""

def ml_skill(savings):
    """given an integer input on amount saved, return a tuple of recommended buy/sell stocks"""
    print("Give it 10 seconds to train model with latest financial day")
    import pandas_datareader.data as web
    import pandas as pd  
    
    #List of stock companies
    alist = ['CSCO', 'QCOM', 'SQ', 'ADTN', 'TWTR', 'AMD', 'EBAY', 'GE', 'GOOG', 'ARCO', 'SAN', 'RUN', 'SND', 'XPLR',
             'JILL', 'WSTL', 'UIS', 'TGH', 'KEM', 'NEXA', 'CNDT', 'BLDR', 'APTO', 'HALO', 'PIRS', 'XOM', 'CVX',
             'NATH', 'YUM', 'BAC', 'WTW', 'AMAT', 'SCHW', 'CUB', 'DLPH', 'DXC', 'AMP', 'COF', 'F', 'MSFT', 'SGH', 'NTNX',
             'ABMD']
    actual_names = ['cisco','qualcomm', 'square', 'adtran', 'twitter','advanced micro devices', 'ebay', 'ge', 'google',
                    'Arcos Dorados Holding', 'Banco Santander', 'sunrun','smart sand','xplore technologies',
                    'jill', 'westell technologies', ' Unisys Corporation', 'Textainer Group Holdings',
                    'KEMET Corporation', 'Nexa Resources', 'Cabot Corp', 'Builders FirstSource',
                    'Aptose Biosciences', 'Halozyme Therapeutics', 'Pieris Pharmaceuticals', 'Exxon Mobil Corporation',
                    'Chevron Corporation', 'Nathan"s Famous','yum brands', 'bank of america', 'Weight Watchers International',
                    'Applied Materials', 'Charles Schwab Corporation', 'Cubic Corporation', 'Delphi Technologies',
                    'dxc technologies', 'Ameriprise Financial', 'Capital One Financial Corp', 'Ford Motor Company',
                    'microsoft', ' Smart Global Holdings', 'Nutanix', 'ABIOMED']

    stock_names = {}
    for i in range(0,len(alist)):
        stock_names[alist[i]] = actual_names[i]
    
    Next_day_opening_vals = {}
    current_day_opening_vals = {}
    
    #Makes next day prediction for each company using Robinhood data and SVR
    for each in alist:
        dataset_stock = web.DataReader('{}'.format(each), 'robinhood')
        X_train = dataset_stock.iloc[:-1,[0,1,3,6]]
        y_train = dataset_stock.iloc[1:249,4]
        X_test = dataset_stock.iloc[248:249,[0,1,3,6]]
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        X_train_scale = scaler.fit_transform(X_train)
        X_test_scale = scaler.transform(X_test)
        from sklearn.svm import SVR
        regressor = SVR(kernel = 'rbf')
        regressor.fit(X_train_scale, y_train)
        y_pred = regressor.predict(X_test_scale)
        current_day_opening_vals[each] = pd.to_numeric(dataset_stock.iloc[248,4], errors = 'ignore')
        Next_day_opening_vals[each] = pd.to_numeric(y_pred)
        
    max_count = Next_day_opening_vals[alist[0]]
    min_count = Next_day_opening_vals[alist[0]]
    
    for key, val in Next_day_opening_vals.items():
        if val > max_count:
            max_count = val
        elif val < min_count:
            min_count = val
    
    #Makes recommendations on savings, then tells next day predicted opening price for   
            
    #List Buy and Sell is what you need.
            
    recommendated_stocks_predicted_values = {}
    other_recommendations = {}
    buy = {}
    sell = {}
    if savings > 2 and savings <= 10:
        for key, value in Next_day_opening_vals.items():
            if (value >2 and value <= 10):
                recommendated_stocks_predicted_values[key] = Next_day_opening_vals[key]
      
    elif savings > 10 and savings <= 50:
        for key, value in Next_day_opening_vals.items():
            if (value >10 and value <=30):
                recommendated_stocks_predicted_values[key] = Next_day_opening_vals[key]
            if (value >2 and value <= 25):
                other_recommendations[key] = Next_day_opening_vals[key]
        
    elif savings > 50 and savings <= 100:
        for key, value in Next_day_opening_vals.items():
            if (value >50 and value <=100):
               recommendated_stocks_predicted_values[key] = Next_day_opening_vals[key]
            if (value >2 and value <= 50):
                other_recommendations[key] = Next_day_opening_vals[key]
        
    elif savings > 100 and savings <= 500:
        for key, value in Next_day_opening_vals.items():
            if (value >100 and value <=500):
                recommendated_stocks_predicted_values[key] = Next_day_opening_vals[key]
            if (value >2 and value <= 250):
                other_recommendations[key] = Next_day_opening_vals[key]
          
    elif savings > 500:
        for key, value in Next_day_opening_vals.items():
            if value >500 :
                recommendated_stocks_predicted_values[key] = Next_day_opening_vals[key]
            elif (value >10 and value <=1000):
                other_recommendations[key] = Next_day_opening_vals[key]
                
    for key, val in recommendated_stocks_predicted_values.items():
        if val - current_day_opening_vals[key] > 0 :
            sell[stock_names[key]] = val
        else:
            buy[stock_names[key]] = val
    
    for key, val in other_recommendations.items():
         if val - current_day_opening_vals[key] > 0 :
            sell[stock_names[key]] = val
         else:
            buy[stock_names[key]] = val
            
    return(buy,sell)
