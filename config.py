# -*- coding: UTF-8 -*-
import os
import configparser

basedir = os.path.abspath(os.path.dirname(__file__))

# 获取文件的当前路径（绝对路径）
cur_path = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(cur_path, 'config.ini')

#读取数据库配置文件
config = configparser.ConfigParser()
config.read(config_path)

dbhost = str(config.get('database', 'dbhost'))
dbport = str(config.get('database', 'dbport'))
dbname = str(config.get('database', 'dbname'))
dbuser = str(config.get('database', 'dbuser'))
dbpassword = str(config.get('database', 'dbpassword'))
dbcharset = str(config.get('database', 'dbcharset'))

class Config:

    # 配置数据库
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'mysql+pymysql://' +dbuser + ':' + dbpassword + '@' + dbhost + ':' + dbport +'/' + dbname
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # foremail: 'automail@zbwxkj.com'
    # password: "test123@zbwxkj.com"
    # toeamil: "zhicheng.ma@zbwxkj.com,mer163@sina.com"
    # smtpaddress: "smtp.mxhichina.com"
    # smtpport: "465"
    # title: "测试报告"

    # 配置邮件
    MAIL_SERVER = config.get('email','MAIL_SERVER')
    MAIL_PORT = config.get('email','MAIL_PORT')
    MAIL_USE_TLS = config.get('email','MAIL_USE_TLS')
    MAIL_USE_SSL = config.get('email','MAIL_USE_SSL')
    MAIL_USERNAME =  config.get('email','MAIL_USERNAME')
    MAIL_PASSWORD = config.get('email','MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = config.get('email','FLASKY_MAIL_SUBJECT_PREFIX')
    FLASKY_MAIL_SENDER = config.get('email','FLASKY_MAIL_SENDER')
    FLASKY_ADMIN = os.environ.get(config.get('email','FLASKY_ADMIN'))

    print(MAIL_SERVER,MAIL_PORT,MAIL_USE_SSL,MAIL_USE_TLS,MAIL_USERNAME,MAIL_PASSWORD,FLASKY_MAIL_SUBJECT_PREFIX,FLASKY_MAIL_SENDER,FLASKY_ADMIN)

    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 30
    FLASKY_SLOW_DB_QUERY_TIME=0.5

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql+pymysql://' +dbuser + ':' + dbpassword + '@' + dbhost + ':' + dbport +'/' + dbname


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'mysql+pymysql://' +dbuser + ':' + dbpassword + '@' + dbhost + ':' + dbport +'/' + dbname
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://' +dbuser + ':' + dbpassword + '@' + dbhost + ':' + dbport +'/' + dbname

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASKY_MAIL_SENDER,
            toaddrs=[cls.FLASKY_ADMIN],
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class HerokuConfig(ProductionConfig):
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'unix': UnixConfig,

    'default': DevelopmentConfig
}
