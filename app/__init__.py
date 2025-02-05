from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    
    from app.routes import main
    app.register_blueprint(main)
    
    with app.app_context():
        from app.models import User  # Import here to avoid circular import
        db.create_all()
        # Create a default user if none exists
        if not User.query.first():
            default_user = User(username="admin")
            default_user.set_password("admin")
            db.session.add(default_user)
            db.session.commit()
    
    return app