from flask import Flask
app = Flask(__name__, static_path='')
from app import views
