from six.moves.urllib.parse import urljoin
import json
import logging
import requests
from requests import get
import re, uuid
import socket
import PacefinAPI.pacefin_exceptions as ex
import sys


log=logging.getLogger(__name__)

class Pacefin(object):

    _root_url = 'https://pacetrader.pacefin.in'
    _login_url = 'https://pacetrader.pacefin.in/api/v3/user/login'
    
    _default_timeout = 7

    _routes = {
        "api.login": "/api/v3/user/login",
        "api.twofa": "/api/v3/user/twofa",

        # profile
        "api.profile": "/api/v1/user/profile?client_id={ClientId}",
    
        # regular order
        "api.regular.order.place": "/api/v1/orders",
        "api.regular.order.modify": "/api/v1/orders",
        "api.regular.order.cancel": "/api/v1/orders/{oms_order_id}",
    

        # conditional order
        "api.conditional.order.place": "/api/v1/orders/kart",
        "api.conditional.order.modify": "/api/v1/orders/kart",
        "api.conditional.order.cancel": "/api/v1/orders/kart/{oms_order_id}",

        # order book
        "api.pending.orderbook": "/api/v1/orders?type=pending&client_id={ClientId}",
        "api.completed.orderbook": "/api/v1/orders?type=completed&client_id={ClientId}",
        "api.traded.orderbook": "/api/v1/orders?type=traded&client_id={ClientId}",
        "api.historical.orderbook": "/api/v1/order/{oms_order_id}/history?client_id={ClientId}",

        # basket order
        "api.basket.create": "/api/v1/basket",
        "api.basket.fetch": "api/v1/basket?login_id={ClientId}",
        "api.basket.delete": "/api/v1/basket?basket_id={BasketId}&name={BasketName}",
        "api.execute.basket": "/api/v1/orders/kart",
        "api.basket.rename": "/api/v1/basket",

        "api.basket.addInstrument": "/api/v1/basket/order",
        "api.basket.editInstrument": "/api/v1/basket/order",
        "api.basket.deleteInstrument": "/api/v1/basket/order?basket_id={BasketId}&name={BasketName}&order_id={OrderId}",

        # gtt
        "api.gtt.create": "/api/v1/event/gtt",
        "api.gtt.order.fetch": "/api/v1/event/gtt?client_id={ClientId}",
        "api.gtt.order.cancel": "/api/v1/event/gtt/{ClientId}/{Id}",
        "api.gtt.order.modify": "/api/v1/event/gtt",

        # portfolio
        "api.portfolio.positions.daywise": "/api/v1/positions?client_id={ClientId}&type=live",
        "api.portfolio.positions.netwise": "/api/v1/positions?client_id={ClientId}&type=historical",
        "api.portfolio.demate.holdings": "/api/v1/holdings?client_id={ClientId}",
        "api.portfolio.convert.position": "/api/v1/position/convert",

        # contract details
        "api.search.scrip": "/api/v1/search?key={KeyOfInstrument}",
        "api.scrip.info": "/api/v1/contract/{Exchange}?info=scrip&token={InstrumentTokenOfEquity}",

        # option chain
        "api.fetch.option.chain":"/api/v1/optionchain/NFO?token={EquityToken}&num={NumberOfEntries}&price={PriceOfOptions}",

        # ipo
        "api.ipo.all": "/api/v1/tradeipo/get-all-ipo",
        "api.ipo.order.place": "/api/v1/tradeipo/place-order",
        "api.ipo.order.fetch": "/api/v1/tradeipo/fetch-order",
        "api.ipo.order.cancel": "/api/v1/tradeipo/cancel-order",

        # funds
        "api.funds1": "/api/v1/funds/view?client_id={ClientId}&type=all",
        "api.funds2": "/api/v2/funds/view?client_id={ClientId}&type=all",

    }



    try:
        clientPublicIp= " " + get('https://api.ipify.org').text
        if " " in clientPublicIp:
            clientPublicIp=clientPublicIp.replace(" ","")
        hostname = socket.gethostname()
        clientLocalIp=socket.gethostbyname(hostname)
    except Exception as e:
        print("Exception while retriving IP Address,using local host IP address",e)
    finally:
        # clientPublicIp="106.193.147.98"
        clientPublicIp=""
        clientLocalIp="127.0.0.1"
    clientMacAddress=':'.join(re.findall('..', '%012x' % uuid.getnode()))
    accept = "application/json"
    userType = "USER"
    sourceID = "WEB"

    def __init__(self,  api_key=None,timeout=None,clientId=None,client_secret=None, disable_ssl=False, debug=False, proxies=None, session_expiry_hook=None, access_token=None, pool=None, *args, **kwargs ):

        """
        Initialize a new Pacefin Client instance.
        - `root_url` is the root URL for the Pacefin API. Defaults to the staging server.
        - `timeout` is the timeout for the HTTP requests in seconds. Defaults to 7 seconds.
        - `disable_ssl` disables SSL verification for the HTTP requests. Defaults to False.
        - `debug` enables the debug mode. Defaults to False.
        - `proxies` is the proxy configuration for the HTTP requests. Defaults to None.
        - `session_expiry_hook` is the function called when the session expires.
        - `access_token` is the access token for the Pacefin API.
        - `refresh_token` is the refresh token for the Pacefin API.
        
        """
        self.api_key = api_key
        path = Pacefin._root_url
        self.root = path
        self.timeout = timeout or Pacefin._default_timeout
        self.disable_ssl = disable_ssl
        self.debug = debug
        self.proxies = proxies  
        self.access_token = None
        self.refresh_token = None
        self.session_expiry_hook = None
        self.privateKey = None
        self.clientId = None
        self.clint_secret = None
        self.loginId = None
        self.clientName = None
        self.clientEmail = None

        if pool:
            self.reqsession = requests.Session()
            reqadapter = requests.adapters.HTTPAdapter(**pool)
            self.reqsession.mount("https://", reqadapter)
            print("in pool")
        else:
            self.reqsession = requests

        # disable requests SSL warning
        requests.packages.urllib3.disable_warnings()
        

    def requestHeaders(self):
        return{
            "X-ClientLocalIP": self.clientLocalIp,
            "X-ClientPublicIP": self.clientPublicIp,
            "X-MACAddress": self.clientMacAddress,
            "X-PrivateKey": self.privateKey,
            "X-UserType": self.userType,
            "X-SourceID": self.sourceID,
            'P-DeviceType': 'WEB',
            'Content-type': 'application/json',
            'accept': 'application/json',
            'x-authorization-token': self.access_token,

        }
    


    def _request(self, route, method, parameters=None):
        """Make an HTTP request."""
        params = parameters.copy() if parameters else {}
       
        uri =self._routes[route].format(**params)
        url = urljoin(self.root, uri)

        # Custom headers
        headers = self.requestHeaders()


        if self.access_token:
            # set authorization header
        
            auth_header = self.access_token
            headers["Authorization"] = "Bearer {}".format(auth_header)

        if self.debug:
            log.debug("Request: {method} {url} {params} {headers}".format(method=method, url=url, params=params, headers=headers))
    
        try:
            r = requests.request(method,
                                        url,
                                        data=json.dumps(params) if method in ["POST", "PUT"] else None,
                                        params=json.dumps(params) if method in ["GET", "DELETE"] else None,
                                        headers=headers,
                                        verify=not self.disable_ssl,
                                        allow_redirects=True,
                                        timeout=self.timeout,
                                        proxies=self.proxies)
           
        except Exception as e:
            raise e

        if self.debug:
            log.debug("Response: {code} {content}".format(code=r.status_code, content=r.content))

        # Validate the content type.
        if "json" in headers["Content-type"]:
            try:
                data = json.loads(r.content.decode("utf8"))
             
            except ValueError:
                raise ex.DataException("Couldn't parse the JSON response received from the server: {content}".format(
                    content=r.content))

            # api error
            if data.get("error_type"):
                # Call session hook if its registered and TokenException is raised
                if self.session_expiry_hook and r.status_code == 403 and data["error_type"] == "TokenException":
                    self.session_expiry_hook()

                # native errors
                exp = getattr(ex, data["error_type"], ex.GeneralException)
                raise exp(data["message"], code=r.status_code)

            return data
        elif "csv" in headers["Content-type"]:
            return r.content
        else:
            raise ex.DataException("Unknown Content-type ({content_type}) with response: ({content})".format(
                content_type=headers["Content-type"],
                content=r.content))
        


        
    def _deleteRequest(self, route, params=None):
        """Alias for sending a DELETE request."""
        return self._request(route, "DELETE", params)
    def _putRequest(self, route, params=None):
        """Alias for sending a PUT request."""
        return self._request(route, "PUT", params)
    def _postRequest(self, route, params=None):
        """Alias for sending a POST request."""
        return self._request(route, "POST", params)
    def _getRequest(self, route, params=None):
        """Alias for sending a GET request."""
        return self._request(route, "GET", params)



    def setAccessToken(self, access_token):
        """Set the `access_token` received after a successful authentication."""
        self.access_token = access_token
    
    

    def login(self, client_id,password):
        """Login into Pacefin.""" 
        payload ={
        "channel_id": client_id,
        "channel_secret": password
        }
        data = self._postRequest("api.login",payload)
        return data
    

    def generateSession(self,client_id,password,totp):
        """Login into Pacefin.""" 
        login_data=self.login(client_id,password)

        if login_data["status"]=="success":
            payload = {"login_id":client_id,
                    "twofa":[{"question_id":22,"answer":totp}],
                                "twofa_token":login_data["data"]["twofa"]["twofa_token"],"type":"PIN","device_type":"web"
                        }

            data = self._postRequest("api.twofa",payload)
            # if data["status"]=="success":
            #     self.setAccessToken(data["data"]["auth_token"])
                # return data
            return data
        return login_data



    def getProfile(self,client_id):
        """Get Profile details."""
        data = self._getRequest("api.profile",{"ClientId":client_id})
        return data


    def placeOrder(self,orderparams):
        params=orderparams
        for k in list(params.keys()):
            if params[k] is None :
                del(params[k])
        
        orderResponse= self._postRequest("api.regular.order.place", params)
        return orderResponse
    
    def modifyOrder(self,orderparams):
        params=orderparams
        for k in list(params.keys()):
            if params[k] is None :
                del(params[k])
        orderResponse= self._putRequest("api.regular.order.modify", params)
        return orderResponse
    
    def cancelOrder(self,orderparams):
        params=orderparams
        for k in list(params.keys()):
            if params[k] is None :
                del(params[k])
        orderResponse= self._deleteRequest("api.regular.order.cancel", params)
        return orderResponse
    
    # conditional order
    def placeConditionalOrder(self,orderparams):
        params=orderparams
        for k in list(params.keys()):
            if params[k] is None :
                del(params[k])
        orderResponse= self._postRequest("api.conditional.order.place", params)
        return orderResponse
    
    def modifyConditionalOrder(self,orderparams):
        params=orderparams
        for k in list(params.keys()):
            if params[k] is None :
                del(params[k])
        orderResponse= self._putRequest("api.conditional.order.modify", params)
        return orderResponse
    
    def cancelConditionalOrder(self,orderparams):
        params=orderparams
        for k in list(params.keys()):
            if params[k] is None :
                del(params[k])
        orderResponse= self._deleteRequest("api.conditional.order.cancel", params)
        return orderResponse
    


    #  gtt order
    def gttCreateRule(self,createRuleParams):
        params=createRuleParams
        for k in list(params.keys()):
            if params[k] is None :
                del(params[k])
        orderResponse= self._postRequest("api.gtt.create", params)
        return orderResponse['data']['id']
    
    def gttModifyRule(self,modifyRuleParams):
        params=modifyRuleParams
        for k in list(params.keys()):
            if params[k] is None :
                del(params[k])
        orderResponse= self._putRequest("api.gtt.order.modify", params)
        return orderResponse['data']['id']
    
    def gttCancelRule(self,cancelRuleParams):
        params=cancelRuleParams
        for k in list(params.keys()):
            if params[k] is None :
                del(params[k])
        orderResponse= self._deleteRequest("api.gtt.order.cancel", params)
        return orderResponse['data']['id']
    
    def gttFetchRule(self,fetchRuleParams):
        params=fetchRuleParams
        for k in list(params.keys()):
            if params[k] is None :
                del(params[k])
        orderResponse= self._getRequest("api.gtt.order.fetch", params)
        return orderResponse['data']['id']


    # basket order
    def createBasket(self,createBasketParams):
        params=createBasketParams
        for k in list(params.keys()):
            if params[k] is None :
                del(params[k])

        orderResponse= self._postRequest("api.basket.create", params)
        return orderResponse

    def fetchBasket(self,clintId):
        orderResponse= self._getRequest("api.basket.fetch", {"ClientId":clintId})
        return orderResponse
    

    def deleteBasket(self,deleteBasketParams):
        params=deleteBasketParams
        for k in list(params.keys()):
            if params[k] is None :
                del(params[k])
        orderResponse= self._deleteRequest("api.basket.delete", params)
        return orderResponse
    
    def addBasketInstrument(self,addBasketInstrumentParams):
        params=addBasketInstrumentParams
        for k in list(params.keys()):
            if params[k] is None :
                del(params[k])
        orderResponse= self._postRequest("api.basket.addInstrument", params)
        return orderResponse
    
    def editBasketInstrument(self,editBasketInstrumentParams):
        params=editBasketInstrumentParams
        for k in list(params.keys()):
            if params[k] is None :
                del(params[k])
        orderResponse= self._putRequest("api.basket.editInstrument", params)
        return orderResponse
    
    def deleteBasketInstrument(self,deleteBasketInstrumentParams):
        params=deleteBasketInstrumentParams
        for k in list(params.keys()):
            if params[k] is None :
                del(params[k])
        orderResponse= self._deleteRequest("api.basket.deleteInstrument", params)
        return orderResponse
    
    def executeBasket(self,executeBasketParams):
        params=executeBasketParams
        for k in list(params.keys()):
            if params[k] is None :
                del(params[k])
        orderResponse= self._postRequest("api.execute.basket", params)
        return orderResponse
    
    def renameBasket(self,renameBasketParams):
        params=renameBasketParams
        for k in list(params.keys()):
            if params[k] is None :
                del(params[k])
        orderResponse= self._putRequest("api.basket.rename", params)
        return orderResponse
    

    # order book
    def getPendingOrderBook(self,client_id):
        """Get Pending Order Book."""
        data = self._getRequest("api.pending.orderbook",{"ClientId":client_id})
        return data
    
    def getCompletedOrderBook(self,client_id):
        """Get Completed Order Book."""
        data = self._getRequest("api.completed.orderbook",{"ClientId":client_id})
        return data

    def getTradedOrderBook(self,client_id):
        """Get Traded Order Book."""
        data = self._getRequest("api.traded.orderbook",{"ClientId":client_id})
        return data
    
    def getHistoricalOrderBook(self,client_id,oms_order_id):
        """Get Historical Order Book."""
        data = self._getRequest("api.historical.orderbook",{"ClientId":client_id,"oms_order_id":oms_order_id})
        return data
    
    

    # portfolio
    def getPositionsDaywise(self,client_id):
        """Get Positions Daywise."""
        data = self._getRequest("api.portfolio.positions.daywise",{"ClientId":client_id})
        return data

    def getPositionsNetwise(self,client_id):
        """Get Positions Netwise."""
        data = self._getRequest("api.portfolio.positions.netwise",{"ClientId":client_id})
        return data
    
    def getDemateHoldings(self,client_id):
        """Get Demate Holdings."""
        data = self._getRequest("api.portfolio.demate.holdings",{"ClientId":client_id})
        return data
    
    def convertPosition(self,convertPositionParams):
        params=convertPositionParams
        for k in list(params.keys()):
            if params[k] is None :
                del(params[k])
        orderResponse= self._putRequest("api.portfolio.convert.position", params)
        return orderResponse
    
    # contract details
    def searchScrip(self,key):
        """Search Scrip."""
        data = self._getRequest("api.search.scrip",{"KeyOfInstrument":key})
        return data

    def getScripInfo(self,exchange,token):
        """Get Scrip Info."""
        data = self._getRequest("api.scrip.info",{"Exchange":exchange,"InstrumentTokenOfEquity":token})
        return data
    
    # option chain
    def getOptionChain(self,equityToken,numberOfEntries,price):
        """Get Option Chain."""
        data = self._getRequest("api.fetch.option.chain",{"EquityToken":equityToken,"NumberOfEntries":numberOfEntries,"PriceOfOptions":price})
        return data
    
    # ipo
    def getAllIPO(self):
        """Get All IPO."""
        data = self._postRequest("api.ipo.all")
        return data
    
    def placeIPOOrder(self,placeIPOOrderParams):
        params=placeIPOOrderParams
        for k in list(params.keys()):
            if params[k] is None :
                del(params[k])
        orderResponse= self._postRequest("api.ipo.order.place", params)
        return orderResponse
    
    def fetchIPOOrder(self,fetchIPOOrderParams):
        params=fetchIPOOrderParams
        for k in list(params.keys()):
            if params[k] is None :
                del(params[k])
        orderResponse= self._postRequest("api.ipo.order.fetch", params)
        return orderResponse
    
    def cancelIPOOrder(self,cancelIPOOrderParams):
        params=cancelIPOOrderParams
        for k in list(params.keys()):
            if params[k] is None :
                del(params[k])
        orderResponse= self._postRequest("api.ipo.order.cancel", params)
        return orderResponse
 
    def getFunds(self,client_id):
        """Get Funds."""
        data = self._getRequest("api.funds1",{"ClientId":client_id})
        return data

