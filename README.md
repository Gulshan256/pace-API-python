# PaceFin python 
Pacefin-python is a Python library for interacting with PaceFin's Trading platform  ,that is a set of REST-like HTTP APIs that expose many capabilities required to build stock market investment and trading platforms. It lets you execute orders in real time..



## Usage

```python

from PacefinAPI.pacefin import Pacefin
from config import *

obj=Pacefin()
data=obj.generateSession(clintId,password,"123456") #totp is otp 
setAccessToken=obj.setAccessToken(data["data"]["auth_token"])

data=obj.getProfile(clintId)   

data=obj.getTradedOrderBook("clint id")

getAllIPO=obj.getAllIPO()


getDemateHoldings=obj.getDemateHoldings("clint id")

getPositionsNetwise=obj.getPositionsNetwise("clint id")


fetchBasket=obj.fetchBasket(clintId)


createBasket=obj.createBasket({"login_id":"clint id","name":"testgk","type":"NORMAL","product_type":"ALL","order_type":"ALL"})


renameBasket=obj.renameBasket({"basket_id":"64fa5b85-bf12-4ceb-9a87-08257abec49c","name":"testBasket"})


deleteBasket=obj.deleteBasket({"BasketId":"06a336ad-4ddd-421e-aa90-0480b0d09eb9","BasketName":"testgk"})

PendingOrder=obj.getPendingOrderBook("clint id")

getCompletedOrder=obj.getCompletedOrderBook("clint id")

## !! Place Buy order
placeOrder=obj.placeOrder({
  "exchange": "NSE",
  "instrument_token": "10666",
  "client_id": clintId,
  "order_type": "MARKET",
  "amo": False,
  "price": 34.8,
  "quantity": 1,
  "disclosed_quantity": 0,
  "validity": "DAY",
  "product": "MIS",
  "order_side": "BUY",
  "device": "WEB",
  "user_order_id": 10002,
  "trigger_price": 0,
  "execution_type": "REGULAR"
  })



  # !! SELL order
placeOrder=obj.placeOrder({
  "exchange": "NSE",
  "instrument_token": "10666",
  "client_id": clintId,
  "order_type": "MARKET",
  "amo": False,
  "price": 34.8,
  "quantity": 1,
  "disclosed_quantity": 0,
  "validity": "DAY",
  "product": "MIS",
  "order_side": "SELL",
  "device": "WEB",
  "user_order_id": 10002,
  "trigger_price": 0,
  "execution_type": "REGULAR"
  })
  



  # !! Condition BO  ordering

conditional_order=obj.placeConditionalOrder( {
    "client_id": clintId,
    "device": "WEB",
    "disclosed_quantity": 0,
    "exchange": "NSE",
    "execution_type": "CO",
    "instrument_token": "10666",
    "is_trailing": True,
    "order_side": "BUY",
    "order_type": "LIMIT",
    "price": 77.9,
    "product": "MIS",
    "quantity": 1,
    "square_off_value": 1,
    "stop_loss_value": 1,
    "trailing_stop_loss": "0.05",
    "trigger_price": 0,
    "user_order_id": 10002,
    "validity": "DAY"
  })


sellconditional_order=obj.placeConditionalOrder( {
    "client_id": clintId,
    "device": "WEB",
    "disclosed_quantity": 0,
    "exchange": "NSE",
    "execution_type": "BO",
    "instrument_token": "10666",
    "is_trailing": True,
    "order_side": "SELL",
    "order_type": "LIMIT",
    "price": 77.9,
    "product": "MIS",
    "quantity": 1,
    "square_off_value": 1,
    "stop_loss_value": 1,
    "trailing_stop_loss": "0.05",
    "trigger_price": 0,
    "user_order_id": 10002,
    "validity": "DAY"
  })




modifyConditionalOrder=obj.modifyConditionalOrder( {
      "exchange":"NSE",
      "instrument_token":10666,
      "client_id":"HI0009",
      "order_type":"LIMIT",
      "price":80.9,
      "quantity":1,
      "disclosed_quantity":0,
      "validity":"DAY",
      "product":"MIS",
      "oms_order_id":"20231211-1762","exchange_order_id":"1200000019706097",
      "filled_quantity":0,
      "remaining_quantity":1,
      "last_activity_reference":1386762580344098300,
      "trigger_price":0,
      "stop_loss_value":1,
      "square_off_value":"2",
      "trailing_stop_loss":0,
      "is_trailing":False,
      "execution_type":"BO"
      })


cancelConditionalOrder=obj.cancelConditionalOrder({
      "oms_order_id":"20231211-1897",
      "execution_type":"BO",
      "exchange_order_id":"1200000022379287",
      "leg_order_indicator":"ENTRY",
      "status":"MODIFY_CONFIRMED",
      "client_id":clintId})
  


### Getting start with websocket


from pacefinwebsocket import PacefinSocket
import time


client_id = "clint id"
with open("access_token.txt", "r") as f:
access_token = f.read()

conn = PacefinSocket(client_id,access_token)

ws_status = conn.run_socket()

print("websocket connected ...")
print(ws_status)


conn.subscribe_detailed_marketdata( {'exchangeCode': 1, 'instrumentToken': 3045})
conn.subscribe_snapquote_data({'exchangeCode': 1, 'instrumentToken': 3045})

print("channels subscribed ....")

detailed_market_data = conn.read_detailed_marketdata()
print(detailed_market_data)
snapquote_data = conn.read_snapquote_data()
print(detailed_market_data)


#  unsubscribe from channels
conn.unsubscribe_detailed_marketdata({'exchangeCode': 1, 'instrumentToken': 3045})
conn.unsubscribe_snapquote_data({'exchangeCode': 1, 'instrumentToken': 3045})


```

