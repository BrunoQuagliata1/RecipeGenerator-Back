from app import db, bcrypt
from app.models.models import User
from flask_jwt_extended import create_access_token

def register_user(email, name, password):
    user = User.query.filter_by(email=email).first()
    if user:
        return {"message": "User already exists"}, False

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, name=name, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return {"message": "User created successfully"}, True

def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=email)
        return {"access_token": access_token}, True

    return {"message": "Invalid email or password."}, False
