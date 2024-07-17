from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

from search_module.config import Config
from search_module.utils.elasticsearch_synchronisation import synchronise,ingest_data_to_elasticsearch

db = SQLAlchemy()
Base = automap_base()

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    with app.app_context():
        db.init_app(app)
        Base.prepare(db.engine, reflect=True)
        synchronise(Base) # Add event listenners after each read, update and delete
        ingest_data_to_elasticsearch(db) # In case you will run the script for the first time, it will upload the database into elasticsearch

    # Import the routes later to prevent circular import ( one of many solutions ) 
    from search_module.main.routes import main
    app.register_blueprint(main)
    return app