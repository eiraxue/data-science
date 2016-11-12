import numpy as np
import pandas as pd

# simulate Delta hedging

stockPrice = np.array([40, 40.5, 39.25])
callPrice = np.array([2.7804, 3.0621, 2.3282])
delta = np.array([0.5824, 0.6142, 0.59])
numberOfCalls = 1
unitOfCall = 100

riskFreeRate = 0.08

# investment calc for hedging selling calls--need to buy shares
numberOfShares0 = unitOfCall * numberOfCalls * delta[0]
netInvestmt = numberOfShares0 * stockPrice[0] - numberOfCalls * unitOfCall * callPrice[0]
financingCharge0 = netInvestmt * (np.exp(0.08 / 365) - 1)

print "NetCost[$%6.2f] :Buy %4.2f of shares to hedge shorting %4.2f call" % (
    netInvestmt, numberOfShares0, numberOfCalls)
print "Overnight financing charge : [$%6.2f] " % financingCharge0

# day 1
# overnight profit/loss
netGain = numberOfShares0 * (stockPrice[1] - stockPrice[0]) - numberOfCalls * unitOfCall * (
    callPrice[1] - callPrice[0]) - financingCharge0
print "Overnight profit/loss: [$%4.2f]" % netGain
# need to add more shares to perfect hedge the large delta
numberOfShares1 = unitOfCall * numberOfCalls * delta[1]
extraShares = numberOfShares1 - numberOfShares0
print "Buy %4.2f more shares to rebalance" % extraShares

# calculate in the time series
nDay = len(stockPrice)
columns = ['Day', 'StockPrice', 'CallPrice', 'Delta']
index = np.arange(nDay)
df = pd.DataFrame(columns=columns, index=index)
df['Day'] = df.index
df['StockPrice'] = stockPrice
df['CallPrice'] = callPrice
df['Delta'] = delta
print df.tail()

df['NofShares'] = unitOfCall * numberOfCalls * df['Delta']
df['NetInvestment'] = df['StockPrice'] * df['NofShares'] - unitOfCall * numberOfCalls * df['CallPrice']
df['DailyFinancingCharge'] = df['NetInvestment'] * (np.exp(0.08 / 365) - 1)
df['OvernightPL'] = df['NofShares'].shift(1) * (df['StockPrice'] - df['StockPrice'].shift(1)) \
                    - unitOfCall * numberOfCalls * (df['CallPrice'] - df['CallPrice'].shift(1)) \
                    - df['DailyFinancingCharge'].shift(1)

print df[['NofShares', 'NetInvestment', 'DailyFinancingCharge', 'OvernightPL']]
