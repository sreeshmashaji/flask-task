from flask import Flask
from app.models import db, bcrypt
from app.routes import routes
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    
    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWTManager(app)  

   
    migrate = Migrate(app, db)

   
    app.register_blueprint(routes)

    return app
