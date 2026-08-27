import numpy as np
import pandas as pd
import yfinance as yf

def loadData(option_contracts):
    options = pd.read_csv(option_contracts)
    return options

