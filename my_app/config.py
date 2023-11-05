import os

DB_USERNAME = os.getenv("DB_USERNAME") or "root"
DB_PASSWORD = os.getenv("DB_PASSWORD") or ""
DB_NAME = os.getenv("DB_NAME") or "simulation"
TEST_DB_NAME = os.getenv("TEST_DB_NAME") or "test_simulation"
DB_HOST = os.getenv("DB_HOST") or "127.0.0.1"
DB_PORT = os.getenv("DB_PORT") or "3307"
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
    SQLALCHEMY_DATABASE_URI = f'mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}'
    print(SQLALCHEMY_DATABASE_URI)


class ProductionConfig(Config):
    DEBUG = False
    CSRF_ENABLED = True
    SERVER_NAME = 'example.com'
