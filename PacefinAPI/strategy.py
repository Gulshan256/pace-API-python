import math
from pacefin import Pacefin
from scipy.stats import norm



class ShortStraddle(Pacefin):
    def __init__(self,exchange, token, symbol, expiry_in_year, lots,strik_price,risk_free_interest_rate,volatility):
        super(ShortStraddle, self).__init__()
        self.exchange=exchange
        self.token=token
        self.symbol = symbol
        self.strik_price=strik_price
        self.expiry_in_year = expiry_in_year
        self.lots = lots
        self.risk_free_interest_rate = risk_free_interest_rate
        self.volatility = volatility

    def fetch_stock_price(self):
        try:
            current_price=self.getLtp(self.exchange,self.token)
            return current_price['data']
        except:
            return None

    def execute_strategy(self):
        # Fetch current stock price
        current_price = self.fetch_stock_price()
        # Short Straddle trades
        # put_option_price = self.get_option_price(current_price, "PE")
        # call_option_price = self.get_option_price(current_price, "CE")

        print("black_scholes_put_price: {}".format(self.black_scholes_put_price(current_price)))
        print("black_scholes_call_price: {}".format(self.black_scholes_call_price(current_price)))

        return {"put_option_price":self.black_scholes_put_price(current_price),"call_option_price":self.black_scholes_call_price(current_price)}

    
    # def get_atm(self, strikes):
    #     starting_value = strikes[0]
    #     interval_difference = strikes[1] - strikes[0]
    #     index = math.ceil((self.fetch_stock_price() - starting_value) / interval_difference)
    #     print("index = ", index)
    #     atm_price = strikes[index]
    #     return atm_price

    # def get_option_price(self, stock_price, option_type):
    #     # spread_from_atm = 1
    #     spread_from_atm = 0
    #     option_price = spread_from_atm * stock_price * (100) # assuming 100 shares per lot
    #     return option_price
    
    def black_scholes_call_price(self,stock_price):
        d1 = (math.log(stock_price / self.strik_price) + (self.risk_free_interest_rate + ( self.volatility**2 / 2)) * self.expiry_in_year) / (self.volatility * math.sqrt(self.expiry_in_year))
        d2 = d1 - self.volatility * math.sqrt(self.expiry_in_year)

        call_price = stock_price * norm.cdf(d1) - self.strik_price * math.exp(-self.risk_free_interest_rate * self.expiry_in_year) * norm.cdf(d2)
        return call_price

    def black_scholes_put_price(self,stock_price):
        d1 = (math.log(stock_price /  self.strik_price) + (self.risk_free_interest_rate + (self.volatility**2 / 2)) * self.expiry_in_year) / (self.volatility * math.sqrt(self.expiry_in_year))
        d2 = d1 - self.volatility * math.sqrt(self.expiry_in_year)

        put_price =  self.strik_price * math.exp(-self.risk_free_interest_rate * self.expiry_in_year) * norm.cdf(-d2) - stock_price * norm.cdf(-d1)
        return put_price

# Example usage
exchange="NSE"
token="3045"
symbol = "SBIN" 

expiry_date = 1  # in years
lots = 1  # Number of lots
strike_price = 100  # Strike price
r = 0.05  # Risk-free interest rate
sigma = 0.2  # Volatility


# Create an instance of ShortStraddleAlgo and execute the strategy
algo = ShortStraddle(exchange,token,symbol, expiry_date, lots, strike_price, r, sigma)
result=algo.execute_strategy()
print(result)




class Butterfly:
    pass