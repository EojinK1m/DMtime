

class DefaultConfig(object):
    DEBUG = False
    TESTING = False

class DevelopConfig(DefaultConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:7419553@localhost:3306/unknown_project'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'Fuck im lonely'

class TestConfig(DefaultConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:7419553@localhost:3306/unknown_project'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'Fuck im lonely'
