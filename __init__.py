from flask import Flask
from db import init_db
from auth import auth
from user import user
import random

app = Flask(__name__)
app.secret_key = random.randbytes(16)
mysql = init_db(app)

