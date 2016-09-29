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
