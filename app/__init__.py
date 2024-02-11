from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

bcrypt = Bcrypt()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    bcrypt.init_app(app)
    db.init_app(app)
    JWTManager(app)

    limiter = Limiter(key_func=get_remote_address, default_limits=["3000 per day", "200 per hour"])
    limiter.init_app(app)

    with app.app_context():
        # Import and initialize models and routes
        from .models.models import Recipe, Tag, User, Bookmark
        db.create_all()

        from .routes.recipe_routes import recipe_bp
        app.register_blueprint(recipe_bp)

        from .routes.auth_routes import auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')

    print("Flask app created.")
    return app
