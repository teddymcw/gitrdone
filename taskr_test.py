import unittest
import os

from taskr import app, db
from taskr.models import User
from config import basedir

TEST_DB = 'test.db'

class AddUser(unittest.TestCase):

	def setUp(self):
		app.config['TESTING']
		#line below looks a bit redundant when looking at the config file
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
		self.app = app.test_client()
		db.create_all()

	def tearDown(self):
		db.drop_all()

	def test_user_setup(self):
		new_user = User('messymarv', 'mess@messcalen.org', 'whatshannin')
		db.session.add(new_user)
		db.session.commit()
		test = db.session.query(User).all()
		for t in test:
			t.name
		assert(t.name == 'messymarv')


if __name__ == '__main__':
	unittest.main()