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