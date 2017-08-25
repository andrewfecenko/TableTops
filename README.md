# TableTops

### Installation: ###
`pip2.7 install -r requirements.txt`


You will need [PostgreSQL](https://www.postgresql.org/download/) or another SQLAlchemy compatible database.<br>
Go to the config.py in the main folder and set up the SQLALCHEMY_DATABASE_URI (with your username, password and the name of your table)<br>

You will need a Google Maps JavaScript API Key from [here](https://developers.google.com/maps/documentation/javascript/get-api-key)<br>
Insert this key into the quotes on line 24 of app/server.py<br>
`GOOGLE_API_KEY = ''`

### To run the webserver: ###
`python run.py` in the main folder

### Screenshots ###
![Alt text](/app/static/readme/ExploreSpaces.png?raw=true "Explore Spaces Page")