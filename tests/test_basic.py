import unittest
from app import create_app, db
from app.models import User, Question

class ForumTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with self.app.app_context():
            db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_registration(self):
        with self.app.app_context():
            user = User(username='test', email='test@example.com')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()
            self.assertEqual(User.query.count(), 1)

    def test_post_question(self):
        with self.app.app_context():
            user = User(username='test', email='test@example.com')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()
            q = Question(title='Hello', body='World', author=user)
            db.session.add(q)
            db.session.commit()
            self.assertEqual(Question.query.count(), 1)

if __name__ == '__main__':
    unittest.main()
