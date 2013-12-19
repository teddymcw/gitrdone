import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
#USERNAME = 'admin'
#PASSWORD = 'pass'
SECRET_KEY = 'hardtotell'
#still proper database path, that is to .db file itself
DATABASE_PATH = os.path.join(basedir, DATABASE)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH

