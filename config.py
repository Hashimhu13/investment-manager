import os
import secrets

class Config:
    SECRET_KEY = secrets.token_hex(16)  # Generate a secure random secret key
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'investment.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False