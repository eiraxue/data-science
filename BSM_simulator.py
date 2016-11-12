# Monte Carlo valuation of European call option in Black-scholes-merton model

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


def BSM(S0, K, T, r, sigma, numberOf, numberOfPath):

    # Valuation AlgorithmA
    z = np.random.standard_normal(numberOfPath)  # Pseudo-random numbers
    ST = S0 * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * z)
    maximum = np.vectorize(lambda x, y: max(x - K, y))
    hT = maximum(ST, 0)
    plotPrices(ST)
    C0 = np.exp(-r * T) * sum(hT) / numberOfPath
    print "value of the European call option %5.3f" % C0
    return C0


def plotPrices(x):
    # the histogram of the data
    n, bins, patches = plt.hist(x, 100, normed=1, facecolor='green', alpha=0.75)
    plt.xlabel('The option price at T')
    plt.ylabel('Probability')
    plt.title(r'$\mathrm{Histogram\ of\ ST}\ \mu=?,\ \sigma=?$')
    plt.axis([20, 200, 0, 0.02])
    plt.grid(True)
    plt.show()


# Set parameters in the BSM
S0 = 100.  # initial index level
K = 105.  # strike price
T = 1.0  # time-to-maturity
r = 0.05  # riskless short rate
sigma = 0.2  # volatility

M = 50  # total number of time steps
dt = T / M  # length of time interval

NumberOfPath = 1000000  # number of simulation paths in MC

print BSM(S0, K, T, r, sigma, NumberOfPath)
