import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TESTING = True

ADMINS = frozenset(['namul10@gmail.com'])
SECRET_KEY = 'VERYVERYSECRET'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')
DATABASE_CONNEXT_OPTIONS = {}


