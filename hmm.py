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

beginDate ='2015-01-01'
endDate = '2015-01-01'
NofHiddenStates = 6

data = get_price('CSI300.INDX', start_date = beginDate, end_date=endDate, frequency='1d')
data[0:9]

