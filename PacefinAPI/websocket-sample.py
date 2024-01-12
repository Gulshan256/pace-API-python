from pacefinwebsocket import PacefinSocket
import time



if __name__ == '__main__':

	client_id = "HI0009"
	with open("access_token.txt", "r") as f:
		access_token = f.read()
	conn = PacefinSocket(client_id,access_token)
	
	ws_status = conn.run_socket()

	print("websocket connected ...")
	print(ws_status)

	marketdata_payload= {'exchangeCode': 1, 'instrumentToken': 3045}
	# marketdata_payload_1= {'exchangeCode': 1, 'instrumentToken': 3499}
	snapquotedata_payload = {'exchangeCode': 1, 'instrumentToken': 3045}
	# conn.subscribe_detailed_marketdata(marketdata_payload,)
	# conn.subscribe_detailed_marketdata(marketdata_payload_1,)
	# conn.subscribe_snapquote_data(snapquotedata_payload,)


	# print("channels subscribed ....")

	# detailed_market_data = conn.read_detailed_marketdata()

	# print("detailed market data", detailed_market_data)

	conn.subscribe_multiple_detailed_marketdata([{'exchangeCode': 1, 'instrumentToken': 3499},{'exchangeCode': 1, 'instrumentToken': 3045}])

	print("multiple channels subscribed ....")

	detailed_market_data = conn.read_multiple_detailed_marketdata()

	print("multiple detailed market data", detailed_market_data)

	# unsubscribe multiple channels
	conn.unsubscribe_multiple_detailed_marketdata([{'exchangeCode': 1, 'instrumentToken': 3499},{'exchangeCode': 1, 'instrumentToken': 3045}])



	# while True:
	# 	time.sleep(1)
	# 	detailed_market_data = conn.read_detailed_marketdata()
	# 	# print(detailed_market_data)
	# 	# time.sleep(1)
	# 	# snapquote_data = conn.read_snapquote_data()
	# 	# print(detailed_market_data)
	# 	i = i + 1
	# 	print("==================================")
	# 	# if i > 5:
	# 	# 	print("unsubscribe marketdata")
	# 	# 	conn.unsubscribe_detailed_marketdata(marketdata_payload)
	# 	# 	print("unsubscribe snapquote")
	# 	# 	conn.unsubscribe_detailed_marketdata(snapquotedata_payload)

			