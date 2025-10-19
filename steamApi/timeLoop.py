from steamApi import getAllGameIDs, getUserFromID, getUserPrice, emailCall, getGamePrice
import time

def runCheck():
    #outside runs until stopped
    while True:
        accumulator = 0
        gameIds = getAllGameIDs()

        for gameId in gameIds:
            priceData = getGamePrice(gameId)
            accumulator += 1

            #only 60 calls per hour, so stop checking once api hourly limit is reached
            if accumulator >= 60:
                print("API limit reached for the hour. Going to sleep.")
                time.sleep(3600)
                accumulator = 0

            if not priceData or priceData[0] is None: #skip
                continue

            #parse
            currPrice = float(priceData[0]) 
            gameTitle = priceData[1]
            usersTracking = getUserFromID(gameId)

            for email in usersTracking:
                trackedGames = getUserPrice(email)

                for j, target in trackedGames:
                    if str(j) == str(gameId):
                        targetPrice = float(target)
                        if currPrice <= targetPrice: #affordable
                            print(f"Sending email to {email} for {gameTitle} at ${currPrice}")
                            emailCall(email, gameId)
        
        print("Finished checking all games. Sleeping for 1 hour.")
        time.sleep(3600)