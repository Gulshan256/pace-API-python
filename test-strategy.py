import datetime
import math

class Straddle:
    def __init__(self, underlying_symbol, strike_price, expiration_date, price_call, price_put):
        """
        'self.underlying_symbol' is the symbol of the underlying asset.
        'self.strike_price' is the strike price of the option.
        'self.expiration_date' is the expiration date of the option.
        'self.price_call' is the price of the call option.
        'self.price_put' is the price of the put option.

        """
        self.underlying_symbol = underlying_symbol
        self.strike_price = strike_price
        self.expiration_date = expiration_date
        self.price_call = price_call
        self.price_put = price_put

        

    def calculate_cost(self):
        """Calculates the total cost of the straddle."""
        return self.price_call + self.price_put

    def calculate_profit_loss(self, underlying_price):
        """Calculates the profit or loss at a given underlying price."""
        call_payoff = max(underlying_price - self.strike_price, 0) - self.price_call
        put_payoff = max(self.strike_price - underlying_price, 0) - self.price_put
        return call_payoff + put_payoff

    def get_days_to_expiration(self):
        """Calculates the number of days until expiration."""
        today = datetime.date.today()
        return (self.expiration_date - today).days

    def get_ltp(self):
        ltp= self.getLtp(self.exchange, self.token)
        return ltp

    def cal_ATM(self):
        """Calculates the ATM price for the straddle and return the ATM price"""
        starting_value = self.strike_price[0]
        interval_difference = self.strike_price[1] - self.strike_price[0]
        index = math.ceil((self.getLtp(self.exchange, self.token)['data'] - starting_value) / interval_difference)
        print("index = %d" % index)
        atm_price = self.strike_price[index]
        return atm_price
    
    def long_straddle_payoff(self, underlying_price):
        """Calculates the payoff of a long straddle strategy."""
        call_payoff = max(underlying_price - self.strike_price, 0) - self.price_call
        put_payoff = max(self.strike_price - underlying_price, 0) - self.price_put
        return call_payoff + put_payoff
    
    def short_straddle_payoff(self, underlying_price):
        """Calculates the payoff of a short straddle strategy."""
        call_payoff = min(self.price_call, max(underlying_price - self.strike_price, 0)) - self.price_call
        put_payoff = min(self.price_put, max(self.strike_price - underlying_price, 0)) - self.price_put
        return call_payoff + put_payoff
    

straddle = Straddle("AAPL", 150, datetime.date(2024, 3, 15), 10, 8)
cost = straddle.calculate_cost()  
print("Cost: ", cost)
profit_at_170 = straddle.calculate_profit_loss(170)  
print("Profit at 170: ", profit_at_170)
days_to_expiry = straddle.get_days_to_expiration()
print("Days to expiry: ", days_to_expiry)
long_straddle_payoff = straddle.long_straddle_payoff(170)
print("Long straddle payoff: ", long_straddle_payoff)
short_straddle_payoff = straddle.short_straddle_payoff(170)
print("Short straddle payoff: ", short_straddle_payoff)




# ----------------------------------------------------------------
#  





# import math

# class Strike:
#     def __init__(self, strike_price):
#         self.strike_price = strike_price

# def spot_index(spot_price, strikes):
#     starting_value = strikes[0].strike_price
#     interval_difference = strikes[1].strike_price - strikes[0].strike_price

#     # Using AP series formula
#     # value = (a + (n-1) * d)
#     # where value is the spot_price, a is the starting value, d is the difference, and n is the index of the spot_price

#     # (spot_price - starting_value) / interval_difference = n-1
#     # n = ((spot_price - starting_value) / interval_difference) + 1

#     index = math.ceil((spot_price - starting_value) / interval_difference)
#     print("Index: %d" % index)
#     print(f"spot price = {spot_price} and startValue is {starting_value} and intervalDifference is {interval_difference} and interval is {index}")
    
#     # Clamp the index to prevent it from going beyond the range of strikes
#     return min(max(index, 0), len(strikes))

# # Example usage:
# strikes = [Strike(strike_price=50), Strike(strike_price=100), Strike(strike_price=150), Strike(strike_price=200), Strike(strike_price=250), Strike(strike_price=300), Strike(strike_price=350)]
# spot_price = 200
# result = spot_index(spot_price, strikes)
# print(result)


"""
class Straddle:
    def __init__(self, underlying_asset, expiration_date, position_size):
        self.underlying_asset = underlying_asset
        self.expiration_date = expiration_date
        self.position_size = position_size
        self.strike_price = None  # To be set later

    def calculate_atm_strike(self, current_price):
        # In a simple example, the ATM strike is set to the current market price
        self.strike_price = current_price

    def execute_straddle(self, call_option_price, put_option_price):
        # Ensure that the ATM strike price has been set
        if self.strike_price is None:
            raise ValueError("ATM strike price not set. Call calculate_atm_strike first.")

        # Calculate the total cost of the straddle
        total_cost = (call_option_price + put_option_price) * self.position_size

        # Display the details of the straddle
        print("\nStraddle Details:")
        print(f"Underlying Asset: {self.underlying_asset}")
        print(f"ATM Strike Price: {self.strike_price}")
        print(f"Expiration Date: {self.expiration_date}")
        print(f"Position Size: {self.position_size}")
        print(f"Total Cost: {total_cost}")

# Example of usage by the client
if __name__ == "__main__":
    # Client creates an instance of Straddle
    straddle_instance = Straddle(
        underlying_asset="XYZ",
        expiration_date="2022-01-01",
        position_size=1
    )

    # Assume the current market price is $105, calculate and set the ATM strike
    straddle_instance.calculate_atm_strike(current_price=105)

    # Client calls the execute_straddle method and passes option prices
    straddle_instance.execute_straddle(call_option_price=5.0, put_option_price=4.0)


"""