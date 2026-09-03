from scipy.optimize import brentq
from Black_scholes import callOption, putOption

def solveIV(S, K, T, r, option_type, market_price):
    if option_type == "call":
        pricing_type = callOption
    elif option_type == "put":
        pricing_type = putOption
    else:
        raise ValueError(f"Unknown option type: {option_type}")

    return brentq(
        lambda sigma: pricing_type(S, K, T, r, sigma) - market_price,
        0.00001,
        5
    )