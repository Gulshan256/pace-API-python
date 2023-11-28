import sys
sys.path.append('./')
from PacefinAPI.pacefin import Pacefin
from config import *
if __name__ == '__main__':
    obj=Pacefin()
    data=obj.generateSession(clintId,password,"123456") #totp is otp 
    setAccessToken=obj.setAccessToken(data["data"]["auth_token"])

    # data=obj.getProfile(clintId)
    # print(data)
    data=obj.getFunds(clintId)
    print(data)
    # data=obj.getPendingOrderBook("clint id")
    # print(data)
    # data=obj.getCompletedOrderBook("clint id")
    # print(data)
    # data=obj.getTradedOrderBook("clint id")
    # print(data)
    # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # getAllIPO=obj.getAllIPO()
    # print(getAllIPO)
    # getDemateHoldings=obj.getDemateHoldings("clint id")
    # print(getDemateHoldings)
    # getPositionsNetwise=obj.getPositionsNetwise("clint id")
    # print(getPositionsNetwise)
    # fetchBasket=obj.fetchBasket(clintId)
    # print(fetchBasket)
    # renameBasket=obj.renameBasket({"basket_id":"64fa5b85-bf12-4ceb-9a87-08257abec49c","name":"hh"})
    # print(renameBasket)
    # createBasket=obj.createBasket({"login_id":"clint id","name":"testgk","type":"NORMAL","product_type":"ALL","order_type":"ALL"})
    # print(createBasket)
    # deleteBasket=obj.deleteBasket({"BasketId":"06a336ad-4ddd-421e-aa90-0480b0d09eb9","BasketName":"testgk"})
    # print(deleteBasket)

    ## !! Place Buy order
    # placeOrder=obj.placeOrder({"exchange": "NSE","instrument_token": "10666","client_id": clintId,"order_type": "MARKET","amo": False,# "price": 34.8,"quantity": 1,"disclosed_quantity": 0,"validity": "DAY","product": "MIS","order_side": "BUY","device": "WEB","user_order_id": 10002,"trigger_price": 0,"execution_type": "REGULAR"})
    # print(placeOrder)

    # # !! SELL order
    # placeOrder=obj.placeOrder({"exchange": "NSE","instrument_token": "10666","client_id": clintId,"order_type": "MARKET","amo": False,"price": 34.8,"quantity": 1,"disclosed_quantity": 0,"validity": "DAY","product": "MIS","order_side": "SELL","device": "WEB","user_order_id": 10002,"trigger_price": 0,"execution_type": "REGULAR"})
    # print(placeOrder)

    





