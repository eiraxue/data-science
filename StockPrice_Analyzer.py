import numpy as np
import pandas as pd
from pandas_datareader import data, wb
import matplotlib.pyplot as plt

# retrieve data from google site
goog = data.DataReader('GOOG', data_source='google', start='3/14/2009', end='4/14/2014')
print goog.tail()

# process the stock index, to get log_ret
goog['Log_Ret'] = np.log(goog['Close'] / goog['Close'].shift(1))
goog['Volatility'] = pd.rolling_std(goog['Log_Ret'], window=252) * np.sqrt(252)

plt.figure()
goog[['Close', 'Volatility']].plot(subplots=True, color='blue', figsize=(8, 6))
