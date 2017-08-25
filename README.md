# TableTops

TableTops looks to turn office spaces into communities of likeminded individuals or small businesses. If you are looking for a place to get inspired, meet people with similar interests and get your independent work done then you’ve come to the right place. Coworking is about sharing your work environment while working independently. Take a look around and you’ll find plenty of spaces in your area that you can become a part of. <br>

If you are a land lord and want to open up a new coworking space or are just looking to fill a few seats then TableTops will help you get there. Create a new office space, upload some pictures and we’ll expose you to hundreds of tenants looking for office space.

#### Technical Features ####
Login/Logout<br>
Administrative functions<br>
In-app messaging<br>
Google Maps JavaScript API integration<br>
Data persistence with PostgreSQL<br>
File uploading<br>
Searching<br>
Search result filtering/querying/sorting<br>
User and rental space reviewing<br>
In-app rental applications<br>


### Installation: ###
This app only works with Python 2.x <br>
It will not work with Python 3.x <br>
`pip2.7 install -r requirements.txt`


You will need [PostgreSQL](https://www.postgresql.org/download/) or another SQLAlchemy compatible database.<br>
Go to the config.py in the main folder and set up the SQLALCHEMY_DATABASE_URI (with your username, password and the name of your table)<br>

You will need a Google Maps JavaScript API Key from [here](https://developers.google.com/maps/documentation/javascript/get-api-key)<br>
Insert this key into the quotes on line 24 of app/server.py<br>
`GOOGLE_API_KEY = ''`<br>

#### Populating your database with samples: ####
`python2.7 db_create.py` in the main folder

### Running the webserver: ###
`python run.py` in the main folder <br>
The website can be accessed [here](127.0.0.1:5000)<br>

### Screenshots ###
![Alt text](/app/static/readme/ExploreSpaces.png?raw=true "Explore Spaces Page")
![Alt text](/app/static/readme/SpaceDescription.png?raw=true "Space Description")
![Alt text](/app/static/readme/AddSpace.png?raw=true "Add Space")