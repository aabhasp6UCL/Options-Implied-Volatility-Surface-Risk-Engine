import numpy as np
import panda as pd
import yfinance as yf

def cleanData(options,usTreasury):

    unique_expirations = options["expiration"].unique()

    for expiration in unique_expirations:
        filtered_options = options[options["expiration"] == expiration]
    
    bid_ask = filtered_options["ask"] > filtered_options["bid"]

    for isGreater in bid_ask:
        filtered_options = filtered_options[isGreater]

    filtered_options["market_price"] = (filtered_options["bid"] + filtered_options["ask"])/2   

    # Calculate and add r to the data frame

    rates = pd.read_csv(usTreasury)
    rates["Date"] = pd.to_datetime(rates["Date"])
    filtered_options["quote_date"] = pd.to_datetime(filtered_options["quote_date"])
    filtered_options["expiration"] = pd.to_datetime(filtered_options["expiration"])
    filtered_options["T"] = (filtered_options["expiration"] - filtered_options["quote_date"]).dt.days / 365

    T_rates = np.array([1/12, 2/12, 3/12, 6/12, 1, 2, 3, 5, 7, 10, 20, 30])
    r = []

    for date, T in zip(filtered_options["quote_date"], filtered_options["T"]):
        row = rates[rates["Date"] == date].iloc[0]
        treasury_rates = row[["1 Mo", "2 Mo", "3 Mo", "6 Mo", "1 Yr", "2 Yr", "3 Yr", "5 Yr", "7 Yr", "10 Yr", "20 Yr", "30 Yr"]].to_numpy(dtype=float) / 100
        r.append(np.interp(T, T_rates, treasury_rates))

    filtered_options["r"] = np.array(r)

   # Calculate and add S to the data frame

    underlying = filtered_options["underlying"]
    start_date = filtered_options["quote_date"]
    end_date = filtered_options["expiration"]
    price = []

    for stock,sd,nd in zip(underlying, start_date, end_date):   
        sd = pd.to_datetime(sd)
        nd = pd.to_datetime(nd)

        prices = yf.download(
        stock,
        start=sd,
        end=nd + pd.Timedelta(days=1),
        auto_adjust=False
        )
        S = prices.loc[sd, "Close"]
        price.append(S)

        price = np.array(price)
        filtered_options["S"] = price

    return filtered_options