import os
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    SERVER_NAME = os.environ.get('SERVER_NAME')
    
    SQLALCHEMY_DATABASE_URI = f'mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_FILE_DIR = os.path.join(basedir, 'session_data')

class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql://sql8640891:UgyTnSX6FZ@sql8.freesqldatabase.com:3306/sql8640891' or Config.SQLALCHEMY_DATABASE_URI
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or Config.SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_DATABASE_URI = f'mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    print("SQLALCHEMY_DATABASE_URI:", SQLALCHEMY_DATABASE_URI)

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'mysql://sql8643944:eVtvPKRR2y@sql8.freesqldatabase.com:3306/sql8643944'

class ProductionConfig(Config):
    DEBUG = False
    CSRF_ENABLED = True
    SERVER_NAME = 'example.com'
