# Straddle Options Trading Strategy

import numpy as np
import matplotlib.pyplot as plt
import seaborn
import yfinance as yf

def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

ticker = 'PNB.NS'
start_date = '2021-01-01'
end_date = '2023-01-01'
short_window = 40
long_window = 100
# Download historical data for required stock
stock_data = get_stock_data(ticker, start_date, end_date)

print(stock_data.head())



# PNB stock price 
spot_price = 117.05 

# Long put
strike_price_long_put = 110 
premium_long_put = 8.3

# Long call
strike_price_long_call = 110 
premium_long_call = 16.05

# Stock price range at expiration of the put
# sT = np.arange(0,2*spot_price,1) 
sT = np.array(stock_data['Adj Close'])
# print(sT)

# Call payoff
"""sumary_line
We define a function that calculates the payoff from buying a call option. The function takes sT which is a range of possible values of 
stock price at expiration, strike price of the call option and premium of the call option as input. It returns the call option payoff.
"""

def call_payoff(sT, strike_price, premium):
    return np.where(sT > strike_price, sT - strike_price, 0) - premium

payoff_long_call = call_payoff (sT, strike_price_long_call, premium_long_call)
# Plot
fig, ax = plt.subplots()
ax.spines['top'].set_visible(False) # Top border removed 
ax.spines['right'].set_visible(False) # Right border removed
ax.spines['bottom'].set_position('zero') # Sets the X-axis in the center
ax.plot(sT,payoff_long_call,label='Long Call',color='r')
plt.xlabel('Stock Price')
plt.ylabel('Profit and loss')
plt.legend()
plt.show()

# Put payoff
"""sumary_line
We define a function that calculates the payoff from buying a put option. The function takes sT which is a range of possible values of stock
price at expiration, strike price of the put option and premium of the put option as input. It returns the put option payoff.
"""


def put_payoff(sT, strike_price, premium):
    return np.where(sT < strike_price, strike_price - sT, 0) - premium 

payoff_long_put = put_payoff(sT, strike_price_long_put, premium_long_put)
# Plot
fig, ax = plt.subplots()
ax.spines['top'].set_visible(False) # Top border removed 
ax.spines['right'].set_visible(False) # Right border removed
ax.spines['bottom'].set_position('zero') # Sets the X-axis in the center
ax.plot(sT,payoff_long_put,label='Long Put',color='g')
plt.xlabel('Stock Price')
plt.ylabel('Profit and loss')
plt.legend()
plt.show()


# Straddle
# Straddle payoff

payoff_straddle = payoff_long_call + payoff_long_put

print ("Max Profit: Unlimited")
print ("Max Loss:", min(payoff_straddle))
# Plot
fig, ax = plt.subplots()
ax.spines['top'].set_visible(False) # Top border removed 
ax.spines['right'].set_visible(False) # Right border removed
ax.spines['bottom'].set_position('zero') # Sets the X-axis in the center

ax.plot(sT,payoff_long_call,'--',label='Long Call',color='r')
ax.plot(sT,payoff_long_put,'--',label='Long Put',color='g')

ax.plot(sT,payoff_straddle,label='Straddle')
plt.xlabel('Stock Price', ha='left')
plt.ylabel('Profit and loss')
plt.legend()
plt.show()
# Max Profit: Unlimited
# Max Loss: -24.35
