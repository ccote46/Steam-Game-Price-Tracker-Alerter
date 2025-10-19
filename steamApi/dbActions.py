import sqlite3

#Adds user email to database
def addUser(email):
    connection = sqlite3.connect("price_tracker.db")
    cursor = connection.cursor()
    
    cursor.execute("INSERT OR IGNORE INTO users (email) VALUES (?)", (email,))

    connection.commit()
    connection.close()

#gets userid from email (used for referencing games db)
def getUserId(email):
    connection = sqlite3.connect("price_tracker.db")
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0] #return id
    else:
        return None

#returns every game id in game db
def getAllGameIDs():
    connection = sqlite3.connect("price_tracker.db")
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT game_id FROM games")
    rows = cursor.fetchall()

    connection.close()

    # Flatten the result into a list of game_ids
    game_ids = [row[0] for row in rows]
    return game_ids

#gets all users following a gameid
def getUserFromID(gameId):
    connection = sqlite3.connect("price_tracker.db")
    cursor = connection.cursor()

    # find emails of all users tracking game
    cursor.execute('''
        SELECT users.email
        FROM users
        JOIN games ON users.id = games.user_id
        WHERE games.game_id = ?
    ''', (gameId,))

    rows = cursor.fetchall()
    connection.close()

    #return lst of emails
    return [row[0] for row in rows]

#adds a game into games db and max price user is willing to pay
def addUserGame(email, gameId, targetPrice):
    userId = getUserId(email)

    if userId is None:
        print("User not found, please register first.")
        return

    connection = sqlite3.connect("price_tracker.db")
    cursor = connection.cursor()
    
    cursor.execute("INSERT INTO games (user_id, game_id, target_price) VALUES (?, ?, ?)", (userId, gameId, targetPrice))
    connection.commit()
    connection.close()

#gets users price in games db
def getUserPrice(user):
    connection = sqlite3.connect("price_tracker.db")
    cursor = connection.cursor()
    
    cursor.execute("SELECT id FROM users WHERE email = ?", (user,))
    result = cursor.fetchone()
    
    if not result:
        connection.close()
        return []
    
    userId = result[0]
    cursor.execute("SELECT game_id, target_price FROM games WHERE user_id = ?", (userId,))
    rows = cursor.fetchall()
    connection.close()
    
    return rows

#remove game from users track list
def removeUserGame(email, gameId):
    userId = getUserId(email)
    
    if userId is None:
        print("User not found.")
        return False
    
    connection = sqlite3.connect("price_tracker.db")
    cursor = connection.cursor()
    
    cursor.execute("DELETE FROM games WHERE user_id = ? AND game_id = ?", (userId, gameId))
    deleted = cursor.rowcount
    
    connection.commit()
    connection.close()
    
    if deleted > 0:
        print(f"Removed game {gameId} from tracking")
        return True
    else:
        print("Game not found in your tracking list")
        return False
    

#clear everything
def clearAllData():
    connection = sqlite3.connect("price_tracker.db")
    cursor = connection.cursor()
    
    cursor.execute("DELETE FROM games")
    cursor.execute("DELETE FROM users")
    
    connection.commit()
    connection.close()
    print("All data cleared from database")