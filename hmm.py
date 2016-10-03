# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 22:14:44 2016

Tested hmm model on IBM, 50% profit from 2005~2016 with 4 hidden states

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


NofHiddenStates = 4
startDate = datetime.datetime(2010, 1, 1)
endDate = datetime.datetime(2016, 1, 27)
stockData = data.DataReader('ibm', data_source='yahoo', start=startDate, end=endDate)
print stockData.head()


#stockData['Log_Ret'] = np.log(stockData['Close']/stockData['Close'].shift(1))
#stockData['Volatility'] = pd.rolling_std(stockData['Log_Ret'], window=252)*np.sqrt(252)
#%matplotlib inline
#stockData[['Close', 'Volatility']].plot(subplots=True, color='blue', figsize=(8,6))

# note that their is stock split during Mar 26th till Apr 2nd
print stockData.loc['2014-03-26':'2014-04-02']
#print stockData.index
#stockData.drop(stockData.index[['2014-03-26','2014-03-27','2014-03-28']])
stockData['LogHL'] = np.log(stockData['High']/stockData['Low'])

# calculate 5 days return/volume
stockData['Log_Ret1'] = np.log(stockData['Adj Close']/stockData['Adj Close'].shift(1))
stockData['Log_Ret5'] = np.log(stockData['Adj Close']/stockData['Adj Close'].shift(5))
stockData['Log_Vol5'] = np.log(stockData['Volume']/stockData['Volume'].shift(5))
stockData[['Log_Ret5', 'Log_Vol5']].plot(subplots=True, color='blue', figsize=(8,6))

# construct the training set
A = np.column_stack([stockData[5:]['LogHL'],stockData[5:]['Log_Ret5'],stockData[5:]['Log_Vol5']])

# Initialize the hmm model
model = GaussianHMM(n_components=NofHiddenStates, covariance_type="full", n_iter=10000)
model.fit(A)
hidden_states= model.predict(A)
print hidden_states[0:20]

# plot the simulated state on each day, need to match dimension for pos and stockData
plt.figure(figsize=(25, 18))
for i in range(model.n_components):
    pos = (hidden_states==i)
    plt.plot_date(stockData.index[5:][pos], stockData[5:]['Adj Close'][pos], 'o', label='hidden state %d' % i, lw=2)
    plt.legend(loc="left")

#%% figure out the bull and bear states.
# to interpret what each state represent, bear/bull market? buy shares when see either of the states
# construct dataFrame with a dict
statesRep = pd.DataFrame({'Date':stockData.index[5:], 'Log_Ret1':stockData['Log_Ret1'][5:], 'State':hidden_states}).set_index('Date')
plt.figure(figsize=(25, 18))
for i in range(model.n_components):
    pos = (hidden_states==i)
    pos = np.append(0, pos[:-1])
    statesRep['state_ret%s' % i] = np.multiply(statesRep['Log_Ret1'], pos)
    plt.plot_date(statesRep.index, np.exp(statesRep['state_ret%s' % i].cumsum()), '-', label='hidden state %d' % i, lw=2)
    plt.legend(loc="left")


#%%  combine long(bull states) and short(bear states) strategy to maximize the profit
plt.figure(figsize=(25, 18))
longShares = (hidden_states==0) + (hidden_states==2) #buy the next day
shortShares = (hidden_states==1) #+ (hidden_states==2) # short the next day
longShares = np.append(0, longShares[:-1])
shortShares = np.append(0, shortShares[:-1])
statesRep['ret'] = np.multiply(statesRep['Log_Ret1'], longShares)#-np.multiply(statesRep['Log_Ret1'], shortShares)
plt.plot_date(statesRep.index, np.exp(statesRep['Log_Ret1'].cumsum()), '-g', lw=2)
plt.legend(loc="left")