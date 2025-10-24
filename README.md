# Steam Game Price Tracker/Alerter
By: Charlotte C 😃

--------------------------------------------------------

Ever really wanted to buy a video game but been unable to afford it?
This app allows you to track the price of any steam game, and compare it hourly with a price maximum that you input.
If you can afford the game, then it will send you an email notification so you know to *buy buy buy*!

To set up:

1) Clone this repo
2) Install libraries!
```
pip3 install requests
pip3 install python-dotenv
```
3) Create a .env file and fill in your GGDeals API key, personal gmail, and gmail app password
-https://gg.deals/api/
-https://support.google.com/accounts/answer/185833
4) Run the code!
```
python3 main.py
```
5) Buy as many games as your heart desires

Thanks for stopping by! 👋


--------------------------------------------------------

## How does this work?

I'm so glad you asked! This application consists of 8 files, each with its own unique purpose!

-Main.py
Main.py is the direct user-interface. It handles the interactions between the user, and issues calls to other files which will execute actions. Behind every option on the "menu", there exists a function in main.py that's correlated to it. Each one of those functions also contains a function call to another file (for the sake of organization multiple files were used). In addition to this, main.py also loads our .env file which allows users to hide their API keys when publishing their code online. I've heard countless tales of users accidentally publishing their API keys to GitHub (a NIGHTMARE secnario), which then allows anyone to then use your account. 

-__init__.py
Init.py loads all function calls in the package. It allows methods to be used across files! Really cool stuff.

-api.py
Api.py is unfortunatley a little bit of a misnomer. It's true intention is to parse through a json of every game currently on Steam, and find matches to the users inputted game. From there, it extracts the ID. This is necessacary because the API that is used can only intake gameIDs, and it seemed a bit rediculous to have the user look up the id of every game they wanted to play when they could just type in the name and we could do the work for them. 

-db_setup.py
In db_setup.py, we initalize and setup the two database tables that will be hosted locally on the users machine. There are two tables, users which contains every users email address and id, and games, which stores information about the game the user chose. It has the game id, target price, and user id, which references the ids from our users table. Basically, if someone inputs their info, on the users table they'll be stored at index n. Then, their info will be put in the games table, and the user id value will also be n. This allows us to reference users data from just their email! Super cool stuff.

-dbActions.py
dbActions holds all the actions that we'd want to perform on our tables. We have our add functions, our get functions, and our remove functions. Each is necessacary for a certain aspect of our database manipulation, and can be called from any file in the package.

-emailSend.py
emailSend.py imports the SMTP client and allows us to send emails to notify users of price changes. You can do this through gmail by going to settings-->apps and getting a key 

-priceChecker.py
priceChecker.py is where our api interactions are really hiding. The function getGamePrice sends a request to GGDeals Steam API, and is able to fetch info on the game inputted. It returns the current price and the game name in an array. The second function, emailCall contains the formatting of the message that will be emailed to the user, and a call to the sendEmail function in emailSend.py

-timeLoop.py
timeLoop.py is our continous checker (with some limitations!). GGDeals API currently only allows 60 calls per hour per user, which means that we can only check 60 games per hour. Don't worry though! By storing where we left off at the end of an hour, we're able to move on to the next 60 after an hour wait. This means that we can check up to 1440 games per day! After each game is checked, its current price is compared to the users inputted target price. If the current price is less than the target price, then the alert email is sent! 

