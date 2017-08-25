# TableTops

TableTops looks to turn office spaces into communities of likeminded individuals or small businesses. If you are looking for a place to get inspired, meet people with similar interests and get your independent work done then you’ve come to the right place. Coworking is about sharing you work environment while working independently. Take a look around and you’ll find plenty of spaces in your area that you can become a part of. <br>

If you are a land lord and want to open up a new cowering space or are just looking to fill a few seats then TableTop will help you get there. Create a new office space, upload some pictures and we’ll expose you to hundreds of tenants looking for office space.

### Installation: ###
`pip2.7 install -r requirements.txt`


You will need [PostgreSQL](https://www.postgresql.org/download/) or another SQLAlchemy compatible database.<br>
Go to the config.py in the main folder and set up the SQLALCHEMY_DATABASE_URI (with your username, password and the name of your table)<br>

You will need a Google Maps JavaScript API Key from [here](https://developers.google.com/maps/documentation/javascript/get-api-key)<br>
Insert this key into the quotes on line 24 of app/server.py<br>
`GOOGLE_API_KEY = ''`<br>

#### Populating your database with samples: ####
`python db_create.py` in the main folder

### Running the webserver: ###
`python run.py` in the main folder

### Screenshots ###
![Alt text](/app/static/readme/ExploreSpaces.png?raw=true "Explore Spaces Page")