from steamApi import getGameId, send_email, setup, addUser, addUserGame, emailCall, removeUserGame, getUserId, clearAllData, getUserPrice
from dotenv import load_dotenv
import os

load_dotenv()



def addToDB(email, gameId):
    maxPrice = input("What is the maximum price you would pay for this game? ($DD.CC): ")
    try:
        float(maxPrice)  # make sure it's a number
    except ValueError:
        print("Please enter a valid price ($Dollars.Cents)")
        return
    
    addUser(email) 
    addUserGame(email, gameId, maxPrice)

#handler for addtodb
def addGame():
    email = input("Please enter your email: ")
    game = input("Enter the name of the game: ")
    gameId = getGameId(game)
    
    if gameId is None:
        print("Could not find game.")
        return
    
    addToDB(email, gameId)


def removeGame():
    email = input("Enter your email: ")
    game = input("Enter the name of the game you'd like to remove: ")
    gameId = getGameId(game)
    
    if gameId is None:
        print("Could not find game.")
        return
    
    r = removeUserGame(email, gameId)

    if r:
        print("Game removed successfully!")
    else:
        print("Game couldn't be removed/isn't in database. Please check inputs and try again.")



def viewTrackedGames():
    from steamApi import getUserPrice, getGamePrice
    
    email = input("Enter your email: ")
    games = getUserPrice(email)
    
    if not games:
        print("\nYou're not tracking any games.\n")
        return
    
    print("\n===========\n")
    print(f"Tracked games for {email}:")
    print("===========\n")
    
    for game_id, target_price in games:
        price_data = getGamePrice(game_id)
        if price_data and price_data[0] is not None:
            current_price = price_data[0]
            title = price_data[1]
            
            # Show if the price is affordable or not yet
            if float(current_price) <= float(target_price):
                affordable = "Can afford!"
            else:
                affordable = ""
            
            print(f"  - {title} -- {affordable}")
            print(f"    Current: ${current_price} | Target: ${target_price}")
            print()
        else:
            print(f"  - Game ID: {game_id}")
            print(f"    Target: ${target_price} (Price unavailable)")
            print()
    
    print("===========\n")

def deleteInfo():
    print("Are you sure you want to delete EVERYTHING? (Y/N)")
    answer = input("")

    if answer.lower() == 'y':
        print("Deleting info...")
        clearAllData()
    else:
        print("Canceled")
    return 

    

if __name__ == "__main__":
    setup()

    while True:
        print("===========\n")
        print("\nWelcome to the Steam game price tracker!\n")
        print("To begin, chose an option\n")
        print("===========\n")
        print("1: Add a game to track")
        print("2: Remove a game")
        print("3: View your tracked games")
        print("4: Delete your info")
        print("5: Start price monitoring")
        print("6: About")
        print("7: Quit")
        response = input("")

        if response == "1":
            addGame() 
   
        elif response == "2":
            removeGame() 
            
        elif response == "3":
            viewTrackedGames()
            
        elif response == "4":
            deleteInfo() 
            
        #price monitoring
        elif response == "5":
            start_monitoring = input("\nStart continuous price monitoring now? (y/n): ")
            if start_monitoring.lower() == 'y':
                from steamApi.timeLoop import runCheck
                print("\nStarting price monitoring...")
                print("This will check prices every hour.")
                print("Press Ctrl+C to stop.\n")
                try:
                    runCheck()
                except KeyboardInterrupt:
                    print("\nMonitoring stopped.")
        
        #about
        elif response == "6":
            print("==========")
            print("About:")
            print("Hello! I'm Charlotte! I made this as a way to learn about how to interface with APIs, and it quickly evolved way out of scope into databases, SQL, and so much more.")
            print("Overall, I had a really fun time on this project and I hope that if you're using it, you find it useful too!")
            print("==========")
            print("My inspiration for this came when my friends wouldn't stop bugging me to get Expedition: 33, but I only had $25.")
            print("So, I figured I could make a code that would tell me when the game was finally affordable!")
            print("I hope this program helps you get whatever videogame you've been really wanting to buy :)")
            print("If there's any bugs, please message me on github and hopefully I can fix them")
            print("==========")
            print("Thanks!")
            print("Charlotte")

        #quit
        elif response == "7":
            break

        else:
            print("Invalid response, try again.")