import requests
from .emailSend import send_email
import os

def getGamePrice(gameId):
    url = "https://api.gg.deals/v1/prices/by-steam-app-id/"
    params = {
        "ids": f"{gameId}",
        "key": os.getenv('GGDEALS_API_KEY'), #Put your API key here (Go to https://gg.deals/api/)
        "region": "us" #set to whatever region you want currency to be in
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        title = data["data"][f"{gameId}"]["title"]
        retailPrice = data["data"][f"{gameId}"]["prices"]["currentRetail"]
        return [retailPrice, title]
    return None

def emailCall(email, gameId):
    ret = getGamePrice(gameId)
    if ret and ret[0] is not None:
        retailPrice = ret[0]
        title = ret[1]
        print(f"{title} is currently ${retailPrice}")
        
        send_email( #Format = subj, body, to, from 
            f"ALERT: Price for {title} is within your budget!!!", 
            f"The current retail price on Steam is ${retailPrice}! Go buy it now!",
            email,
            os.getenv('EMAIL') #put your email here -- needs to match one in emailSend.py
        )
    else:
        print("Error fetching price")