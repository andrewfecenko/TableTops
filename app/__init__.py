import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import basedir


app = Flask(__name__)
app.config.from_object('config')
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)




from app import server, forms, models
