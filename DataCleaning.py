import numpy as np
import pandas as pd  # pyright: ignore[reportMissingImports]
import importlib

def cleanData(options, usTreasury):
    try:
        yf = importlib.import_module("yfinance")
    except ImportError as exc:
        raise ImportError(
            "yfinance is required. Install it with: python -m pip install yfinance"
        ) from exc

    bid_ask = options["ask"] > options["bid"]
    filtered_options = options[bid_ask].copy()
    filtered_options["market_price"] = (filtered_options["bid"] + filtered_options["ask"]) / 2

    # Calculate and add r to the data frame
    rates = pd.read_csv(usTreasury)
    rates["Date"] = pd.to_datetime(rates["Date"])
    filtered_options["quote_date"] = pd.to_datetime(filtered_options["quote_date"])
    filtered_options["expiration"] = pd.to_datetime(filtered_options["expiration"])
    filtered_options["T"] = (filtered_options["expiration"] - filtered_options["quote_date"]).dt.days / 365

    T_rates = np.array([1/12, 2/12, 3/12, 6/12, 1, 2, 3, 5, 7, 10, 20, 30])
    r = []

    for date, T in zip(filtered_options["quote_date"], filtered_options["T"]):
        row = rates[rates["Date"] <= date].iloc[-1]  # nearest published rate on/before quote date
        treasury_rates = row[["1 Mo", "2 Mo", "3 Mo", "6 Mo", "1 Yr", "2 Yr", "3 Yr", "5 Yr", "7 Yr", "10 Yr", "20 Yr", "30 Yr"]].to_numpy(dtype=float) / 100
        r.append(np.interp(T, T_rates, treasury_rates))

    filtered_options["r"] = np.array(r)

    # Calculate and add S to the data frame
    underlying = filtered_options["underlying"]
    start_date = filtered_options["quote_date"]
    cache = {}
    price = []

    for stock, sd in zip(underlying, start_date):
        if (stock, sd) not in cache:
            try:
                prices = yf.download(stock, start=sd - pd.Timedelta(days=7), end=sd + pd.Timedelta(days=1),
                                      auto_adjust=False, multi_level_index=False, progress=False)
                cache[(stock, sd)] = prices.loc[:sd, "Close"].iloc[-1]
            except Exception:
                cache[(stock, sd)] = np.nan
        price.append(cache[(stock, sd)])

    filtered_options["S"] = np.array(price)
    filtered_options = filtered_options.dropna(subset=["S"])

    return filtered_options