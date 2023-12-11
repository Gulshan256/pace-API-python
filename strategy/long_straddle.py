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