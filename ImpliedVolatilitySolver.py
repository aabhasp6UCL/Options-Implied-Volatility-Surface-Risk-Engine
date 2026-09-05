import numpy as np
from Black_scholes import callOption, putOption


def brentq(function, lower, upper, tolerance=1e-12, max_iterations=100):
    """Find a root of a continuous function on a bracket."""
    lower_value = function(lower)
    upper_value = function(upper)

    if lower_value == 0:
        return lower
    if upper_value == 0:
        return upper
    if lower_value * upper_value > 0:
        raise ValueError("Root is not bracketed")

    for _ in range(max_iterations):
        midpoint = (lower + upper) / 2
        midpoint_value = function(midpoint)
        if abs(midpoint_value) <= tolerance or upper - lower <= tolerance:
            return midpoint

        if lower_value * midpoint_value <= 0:
            upper, upper_value = midpoint, midpoint_value
        else:
            lower, lower_value = midpoint, midpoint_value

    return (lower + upper) / 2


def solveIV(S, K, T, r, option_type, market_price):
    if option_type == "call":
        pricing_type = callOption
    elif option_type == "put":
        pricing_type = putOption
    else:
        raise ValueError(f"Unknown option type: {option_type}")

    f = lambda sigma: pricing_type(S, K, T, r, sigma) - market_price

    # Not every quoted price is consistent with a Black-Scholes price in
    # [sigma=0.00001, sigma=5] (bad quotes, arbitrage violations, etc.).
    # brentq requires the endpoints to bracket a root, so guard against
    # that instead of letting one bad row crash the whole pipeline.
    try:
        if f(0.00001) * f(5) > 0:
            return np.nan
        return brentq(f, 0.00001, 5)
    except (ValueError, RuntimeError):
        return np.nan