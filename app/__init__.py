from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'put database URi'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'Put here the secret'
app.config['DEBUG']=True
app.config['DEVELOPMENT']=False
app.config['RECAPTCHA_PUBLIC_KEY']=os.environ['RECAPTCHA_PUBLIC_KEY']
app.config['RECAPTCHA_PRIVATE_KEY']= os.environ['RECAPTCHA_PRIVATE_KEY']
migrate = Migrate(app,db) 

from app.controllers import default





