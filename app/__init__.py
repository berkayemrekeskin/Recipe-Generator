from flask import Flask
from app.recipe import recipe_bp
from app.auth import auth_bp
import random

app = Flask(__name__)
app.secret_key = random.randbytes(16)
app.config['SECRET_KEY'] = 'top_secret'


# Register blueprints

app.register_blueprint(recipe_bp) 
app.register_blueprint(auth_bp)


if __name__ == '__main__':
    app.run(debug=True)
