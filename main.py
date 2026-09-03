import numpy as np

from OptionContractsData import loadData
from DataCleaning import cleanData
from ImpliedVolatilitySolver import solveIV
from PlotSurface import surface

option_contracts = "2013-02-26options.csv"
usTreasury = "par-yield-curve-rates-2010-2019.csv"

options = loadData(option_contracts)
f_options = cleanData(options, usTreasury)

iv = []

for i in range(len(f_options)):
    S = f_options["S"].iloc[i]
    K = f_options["strike"].iloc[i]
    T = f_options["T"].iloc[i]
    r = f_options["r"].iloc[i]
    option_type = f_options["type"].iloc[i]
    market_price = f_options["market_price"].iloc[i]

    volatility = solveIV(S, K, T, r, option_type, market_price)
    iv.append(volatility)

iv = np.array(iv)

surface(iv, f_options)