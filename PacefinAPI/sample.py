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

	marketdata_payload = {'exchangeCode': 1, 'instrumentToken': 3045}
	snapquotedata_payload = {'exchangeCode': 1, 'instrumentToken': 3045}
	conn.subscribe_detailed_marketdata(marketdata_payload,)
	# conn.subscribe_snapquote_data(snapquotedata_payload,)


	# # print("channels subscribed ....")


	i = 0
	while True:
		time.sleep(1)
		detailed_market_data = conn.read_detailed_marketdata()
		print(detailed_market_data)
		time.sleep(1)
		snapquote_data = conn.read_snapquote_data()
		print(detailed_market_data)
		i = i + 1
		print("==================================")
		if i > 5:
			print("unsubscribe marketdata")
			conn.unsubscribe_detailed_marketdata(marketdata_payload)
			print("unsubscribe snapquote")
			conn.unsubscribe_detailed_marketdata(snapquotedata_payload)
			