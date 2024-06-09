"""Run server"""
import os

from dotenv import load_dotenv
from flask import Flask

load_dotenv()
app = Flask(__name__)
APP_SECRET_KEY = os.getenv('APP_SECRET_KEY')
app.config['SECRET_KEY'] = APP_SECRET_KEY
from graficos import routes
