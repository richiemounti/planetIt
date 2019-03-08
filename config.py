import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'P@ssw0rd!'
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@email.com'

    DEMO_PASSWORD = os.environ.get('DEMO_PASSWORD') or 'P@ssw0rd!'
    DEMO_EMAIL = 'demo@email.com'

    DEMO_ADMIN_PASSWORD = os.environ.get('DEMO_ADMIN_PASSWORD') or 'P@ssw0rd!'
    DEMO_ADMIN_EMAIL = 'demo_admin@mail.com'

    DEBUG = False
    TESTING = False
    FLASK_DEBUG = 0
   

    
    


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    


class ProductionConfig(Config):
    DEBUG = False
    


class TestingConfig(Config):
    DEBUG = True
    LOGIN_DISABLED = True



