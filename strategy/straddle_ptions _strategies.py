import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

def generate_signals(stock_data, short_window, long_window):

    """
    This code uses a moving average crossover strategy with short and long moving averages. Buying signals are generated when the short moving
    average crosses above the long moving average, indicating a potential uptrend (long position). Selling signals are generated when the
    short moving average crosses below the long moving average, indicating a potential downtrend (short position).
    """
    

    signals = pd.DataFrame(index=stock_data.index)
    signals['signal'] = 0.0

    # Create short simple moving average
    signals['short_mavg'] = stock_data['Adj Close'].rolling(window=short_window, min_periods=1, center=False).mean()

    # Create long simple moving average
    signals['long_mavg'] = stock_data['Adj Close'].rolling(window=long_window, min_periods=1, center=False).mean()

    # Create signals
    signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)   

    # Generate buying (1) and selling (-1) signals
    signals['positions'] = signals['signal'].diff()

    return signals

def plot_signals(stock_data, signals):
    fig, ax1 = plt.subplots(figsize=(12, 8))

    # Plot stock price
    ax1.plot(stock_data['Adj Close'], label='Stock Price', color='blue')

    # Plot short and long moving averages
    ax1.plot(signals['short_mavg'], label='Short MAVG', color='red', alpha=0.3)
    ax1.plot(signals['long_mavg'], label='Long MAVG', color='green', alpha=0.3)

    # Plot buying signals
    ax1.plot(signals.loc[signals.positions == 1.0].index, 
             signals.short_mavg[signals.positions == 1.0],
             '^', markersize=10, color='g', label='Buy Signal')

    # Plot selling signals
    ax1.plot(signals.loc[signals.positions == -1.0].index, 
             signals.short_mavg[signals.positions == -1.0],
             'v', markersize=10, color='r', label='Sell Signal')

    ax1.set_title('Long and Short Trading Signals with Moving Averages')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Stock Price')
    ax1.legend()

    plt.show()

# Example usage

ticker = 'RELIANCE.NS'
start_date = '2021-01-01'
end_date = '2023-01-01'
short_window = 40
long_window = 100

stock_data = get_stock_data(ticker, start_date, end_date)
signals = generate_signals(stock_data, short_window, long_window)
plot_signals(stock_data, signals)
