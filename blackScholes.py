from yahoo_fin import options
from yahoo_fin import stock_info as si
import numpy as np
from scipy.stats import norm
import pandas as pd
from datetime import *

stock = input("Enter stock symbol: Ex:QQQ ")
#the user input for option expiration must be valid, but it's easy to get 
#from https://www.cboe.com/delayed_quotes/qqq/quote_table
Day = int(input("Enter option expiration day: Ex:8 "))
month = int(input("Enter option expiration month: Ex:11 "))
year = int(input("Enter option expiration year: Ex:2021 "))
today = date.today()
future = date(year,month,Day)
expiry = future
str(future - today)
pd.set_option("display.max_rows", None, "display.max_columns", None)
options.get_options_chain(stock)
chain = options.get_options_chain(stock,expiry)

#the stock price
si.get_live_price(stock)
r = .025
S = si.get_live_price(stock)
K = chain["calls"].Strike
t = float((future - today).days)
T = t/365
s = chain["calls"]['Implied Volatility']
sigma = chain["calls"]["Implied Volatility"].apply(lambda x: float(x[:-1]) / 100)

def blackScholes(r, S, K, T, sigma):
    "Calculate BS option price for a call/put"
    d1 = (np.log(S/K)+(r+sigma**2/2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    try:
            price = S*norm.cdf(d1, 0, 1) - K*np.exp(-r*T)*norm.cdf(d2, 0, 1) 
            #print("Option Delta is: ",norm.cdf(d1, 0, 1))
            return price
    except:
        print("Please confirm all option parameters above!!!")

print(round(blackScholes(r, S, K, T, sigma),2))

#the difference between the option price and the black scholes value
rt = round(blackScholes(r, S, K, T, sigma),2) - chain["calls"]['Last Price']
rt #BS - last

#display the options chain
chain["calls"]
