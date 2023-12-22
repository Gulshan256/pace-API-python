
def long_straddle(stock_price, strike_price, call_premium, put_premium): # Long Straddle - In a long straddle, profit is unlimited and loss is limited.
    # Calculate net debit (premium paid to enter the trade)
    net_debit = call_premium + put_premium

    # Calculate profit/loss scenarios
    if stock_price > strike_price + net_debit:
        # Case 1: Stock price goes up, call is in the money, put expires worthless
        net_profit_loss = net_debit - (stock_price - strike_price)
    elif stock_price < strike_price - net_debit:
        # Case 2: Stock price goes down, put is in the money, call expires worthless
        net_profit_loss = net_debit - (strike_price - stock_price)
    else:
        # Case 3: Stock price remains the same, both options expire worthless
        net_profit_loss = -net_debit

    return net_profit_loss

# Example usage
stock_price = 50
strike_price = 50
call_premium = 200
put_premium = 200

result = long_straddle(stock_price, strike_price, call_premium, put_premium)

print(f"Net Profit/Loss: ${result:.2f}")



def short_straddle_profit_loss(stock_price, strike_price, premium, lot_size):
    # Calculate net credit (premium received from entering the trade)
    net_credit = premium * lot_size

    # Calculate profit/loss at expiration
    profit_loss = net_credit - (abs(stock_price - strike_price) - premium) * lot_size

    return profit_loss

# Example usage
stock_price = 60
strike_price = 40
premium = 2
lot_size = 100

result = short_straddle_profit_loss(stock_price, strike_price, premium, lot_size)

print(f"Profit/Loss: ${result:.2f}")