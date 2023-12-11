import requests
import base64

# Replace with your OAuth 2.0 client ID and client secret
CLIENT_ID = "PACE-CSG981"
# CLIENT_ID = "PACE-HI0009"
CLIENT_SECRET = "<client_secret>"

# Replace with your OAuth 2.0 authorization server base URL
BASE_URL = "https://pacetrader.pacefin.in"

# Replace with your desired scopes
SCOPES = ["orders", "holdings"]

# Replace with your redirect URI
REDIRECT_URI = "http://127.0.0.1/"

# Generate a random state value
STATE = "3unqcjh2DN1o"

# Construct the authorization URL
authorization_url = f"{BASE_URL}/oauth2/auth"
params = {
    "scope": " ".join(SCOPES),
    "state": STATE,
    "redirect-uri": REDIRECT_URI,
    "response_type": "code",
    "client_id": CLIENT_ID,
}

# Redirect the user to the authorization URL
print(authorization_url)
redirect_response = requests.get(authorization_url, params=params)
print(redirect_response.text)
print(redirect_response.status_code)
# Check if the user approved the request
if redirect_response.status_code != 200:
    print("Error: User did not approve the request.")
    exit()



# Extract the authorization code from the redirect URL
code = redirect_response.url.split("code=")[-1]

# Construct the access token endpoint URL
token_endpoint = f"{BASE_URL}/oauth2/token"

# Encode the client ID and client secret in base64
authorization = f"Basic {base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('utf-8')).decode('utf-8')}"

# Build the request body for exchanging the authorization code for an access token
request_body = {
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": REDIRECT_URI,
}

# Make the POST request to the token endpoint
token_response = requests.post(token_endpoint, headers={"Authorization": authorization}, data=request_body)

# Check if the access token was successfully obtained
if token_response.status_code != 200:
    print("Error: Failed to obtain access token.")
    exit()

# Extract the access token from the response
access_token = token_response.json().get("access_token")

# Use the access token to make authorized requests to the API
print(f"Access Token: {access_token}")
