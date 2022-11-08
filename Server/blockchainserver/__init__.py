from flask import Flask
from flask_cors import CORS
import sys
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hgftite565etdyrdi56d@@46747uf'
CORS(app)
from blockchainserver import routes