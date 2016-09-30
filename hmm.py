# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 22:14:44 2016

E.G. https://www.ricequant.com/community/topic/788/
@author: Eira
"""

from hmmlearn.hmm import GaussianHMM
import numpy as np
from matplotlib import cm, pyplot as plt
import matplotlib.dates as dates
import pandas as pd
import datetime
from pandas_datareader import data, wb


NofHiddenStates = 6
startDate = datetime.datetime(2005, 1, 1)
endDate = datetime.datetime(2016, 1, 27)
goog = data.DataReader('goog', data_source='yahoo', start=startDate, end=endDate)
print goog.head()


#goog['Log_Ret'] = np.log(goog['Close']/goog['Close'].shift(1))
#goog['Volatility'] = pd.rolling_std(goog['Log_Ret'], window=252)*np.sqrt(252)
#%matplotlib inline
#goog[['Close', 'Volatility']].plot(subplots=True, color='blue', figsize=(8,6))

# note that their is stock split during Mar 26th till Apr 2nd
print goog.loc['2014-03-26':'2014-04-02']
print goog.index
goog.drop(goog.index[['2014-03-26','2014-03-27','2014-03-28']])
goog['LogHL'] = np.log(goog['High']/goog['Low'])

# calculate 5 days return/volume
goog['Log_Ret5'] = np.log(goog['Adj Close']/goog['Adj Close'].shift(5))
goog['Log_Vol5'] = np.log(goog['Volume']/goog['Volume'].shift(5))
goog[['Log_Ret5', 'Log_Vol5']].plot(subplots=True, color='blue', figsize=(8,6))

# construct the training set
A = np.column_stack([goog[5:]['LogHL'],goog[5:]['Log_Ret5'],goog[5:]['Log_Vol5']])

# Initialize the hmm model
remodel = GaussianHMM(n_components=NofHiddenStates, covariance_type="full", n_iter=5000)
remodel.fit(A)
hidden_states= remodel.predict(A)
print hidden_states[0:20]