import os

class Config : 
    SECRET_KEY= os.environ.get('FLASK_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI= "mysql+pymysql://root:@localhost:3307/"+os.environ.get("DATABASE_NAME")
    SQLALCHEMY_TRACK_MODIFICATIONS= False
