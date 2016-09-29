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
start = datetime.datetime(2005, 1, 1)
end = datetime.datetime(2016, 1, 27)
data = data.DataReader("GOOGL", 'yahoo', start, end)
#('CSI300.INDX', start_date = beginDate, end_date=endDate, frequency='1d')
print data.head()


import numpy as np
import pandas as pd
from pandas_datareader import data, wb
import matplotlib

goog = data.DataReader('goog', data_source='google', start='3/14/2009', end='4/14/2014')
goog.tail()

goog['Log_Ret'] = np.log(goog['Close']/goog['Close'].shift(1))
goog['Volatility'] = pd.rolling_std(goog['Log_Ret'], window=252)*np.sqrt(252)
%matplotlib inline
goog[['Close', 'Volatility']].plot(subplots=True, color='blue', figsize=(8,6))
