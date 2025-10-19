import requests

def getGameId(game):
    url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    try:
        response = requests.get(url)
        response.raise_for_status() #throw error if bad status code
        data = response.json()
    except requests.RequestException as e:
        print(f"Error getting Steam data: {e}")
        return None
    
    
    apps = data['applist']['apps']
    matches = [app for app in apps if game.lower() in app['name'].lower()] #list of all str matching

    if len(matches) > 1:
        print("Multiple matches found, please select the correct one:")
        for i, m in enumerate(matches[:10]):
            print(f"[{i}] {m['name']}")
        matchNo = input("Enter number: ")
        if matchNo.isdigit() and 0 <= int(matchNo) < len(matches[:10]):
            return matches[int(matchNo)]['appid']
        else:
            print("Invalid selection.")
        return None
    elif len(matches) == 0:  #no matches
        return None
    else:  # 1 match
        return matches[0]['appid']