from search_module.config import Config
from search_module.utils.elasticsearch_synchronisation import synchronise

from sqlalchemy.ext.automap import automap_base

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
Base = automap_base()

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    with app.app_context():
        db.init_app(app)
        Base.prepare(db.engine, reflect=True)
        synchronise(Base) # Add event listenners after each read, update and delete

    # Import the routes later to prevent circular import ( one of many solutions ) 
    from search_module.main.routes import main
    app.register_blueprint(main)
    return app