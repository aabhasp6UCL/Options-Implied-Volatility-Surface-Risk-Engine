import numpy as np
import matplotlib.pyplot as plt

def surface(iv, filtered_options):
    strike_price = filtered_options["strike"].to_numpy()
    time = filtered_options["T"].to_numpy()

    valid = np.isfinite(iv)
    strike_price = strike_price[valid]
    time = time[valid]
    iv = iv[valid]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    ax.plot_trisurf(strike_price, time, iv)

    ax.set_xlabel("Strike Price (K)")
    ax.set_ylabel("Time to Expiration (T)")
    ax.set_zlabel("Implied Volatility")

    return plt.show()
    return ax