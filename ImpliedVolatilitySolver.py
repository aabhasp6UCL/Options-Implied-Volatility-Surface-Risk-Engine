import numpy as np
from scipy.optimize import brentq

def solveIV(S,K,T,r,option_type,market_price):
    
    if option_type == "call":
        pricing_type = callOption
    else:
        pricing_type = putOption

    return brentq(pricing_type(S,K,T,r)-market_price,0.00001,5)