import os

class DefaultConfig(object):
    DEBUG = False
    TESTING = False

    DB_USER = os.environ['DMTIME_DB_USER']
    DB_PW = os.environ['DMTIME_DB_PW']
    DB_URI = os.environ['DMTIME_DB_URI']
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PW}@{DB_URI}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ['DMTIME_JWT_KEY']

    IMAGE_UPLOADS = os.environ['DMTIME_IMAGE_STORAGE']
    IMAGES_URL = os.environ['DMTIME_SERVER_NAME']+'/images/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    EMAIL_SENDER_ADDRESS = os.environ['DMTIME_EMAIL_SENDER_ADDRESS']
    EMAIL_PASSWORD = os.environ['DMTIME_EMAIL_PASSWORD']
    EMAIL_SERVER = os.environ['DMTIME_EMAIL_SERVER']
    EMAIL_PORT = os.environ['DMTIME_EMAIL_PORT']
    EMAIL_VERIFY_DEADLINE = 300


class ProductConfig(DefaultConfig):
    pass

class DevelopConfig(DefaultConfig):
    DEBUG = True
    TESTING = True

    ADMIN_LIST = ['eojin.dev@gmail.net', 'vjslzhs6@naver.com']

class TestConfig(DefaultConfig):
    DEBUG = True
    TESTING = True
    JWT_SECRET_KEY = 'Fuck im lonely'
    ADMIN_LIST = ['test_admin']
