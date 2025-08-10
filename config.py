import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
  MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
  MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
  MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in [
      'true', 'on', '1']
  MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
  MAIL_SUBJECT_PREFIX = '[Social Website] '
  APP_ADMIN = os.environ.get('APP_ADMIN')
  MAIL_SENDER = os.environ.get('MAIL_SENDER')
  APP_POSTS_PER_PAGE = 20
  APP_FOLLOWERS_PER_PAGE = 20
  APP_COMMENTS_PER_PAGE = 10
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  @staticmethod
  def init_app(app):
    pass


class DevelopmentConfig(Config):
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = os.environ.get(
      'DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
  TESTING = True
  SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///'
  WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
  SQLALCHEMY_DATABASE_URI = os.environ.get(
      'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

  @classmethod
  def init_app(cls, app):
    Config.init_app(app)
    # email errors to administrators`
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    secure = None
    if getattr(cls, 'MAIL_USERNAME', None) is not None:
      credentials = (cls.MAIL_USERNAME, cls. MAIL_PASSWORD)
      if getattr(cls, 'MAIL_USE_TLS', None):
        secure = ()
    mail_handler = SMTPHandler(
        mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
        fromaddr=cls.MAIL_SENDER,
        toaddrs=[cls.APP_ADMIN],
        subject='[Social Website] Application Error',
        credentials=credentials,
        secure=secure
    )
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
