import unittest
import hashlib
from app import app, db
from app.models import User, News

def get_hashed_password(user_password):
    salt = "cefalologin"
    salted_password = user_password + salt
    hashed_value = hashlib.md5(salted_password.encode())
    return hashed_value.hexdigest()

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI']='mysql://newsroom_db_admin:newsroom_db_password@localhost/newsroom_test_db'
        self.tester = app.test_client(self)
        self.email_address = "test@example.com"
        self.password = "password"
        self.full_name = "Test User"
        self.news_title = "Test Title"
        self.news_body = "Test Body"
        self.news_author = "Test Author"
        self.news_date = "2017-10-02"
        self.news_user_id = "0"
        self.news_id = "0"
        db.create_all()

    def tearDown(self):
        with app.app_context():
            self.delete_user()
            self.delete_news()
            db.session.remove()

    def create_user(self):
        with app.app_context():
            existing_user = User.query.filter_by(email_address=self.email_address).first()
            if existing_user == None:
                new_user = User(
                    email_address=self.email_address,
                    password=get_hashed_password(self.password),
                    full_name=self.full_name)
                db.session.add(new_user)
                db.session.commit()
                return new_user
            return existing_user

    def delete_user(self):
        with app.app_context():
            existing_user = User.query.filter_by(email_address=self.email_address).first()
            if existing_user != None:
                db.session.delete(existing_user)
                db.session.commit()

    def recreate_user(self):
        with app.app_context():
            existing_user = User.query.filter_by(email_address=self.email_address).first()
            if existing_user != None:
                return existing_user
            else:
                return self.create_user()

    def create_news(self):
        with app.app_context():
            existing_user = User.query.filter_by(email_address=self.email_address).first()
            if existing_user == None:
                new_user = User(
                    email_address=self.email_address,
                    password=get_hashed_password(self.password),
                    full_name=self.full_name)
                db.session.add(new_user)
                db.session.commit()
                db.session.refresh(new_user)
                new_user_id = new_user.id
                self.news_user_id = new_user_id
            else:
                new_user_id = existing_user.id
                self.news_user_id = new_user_id
            new_news = News(
                news_title=self.news_title,
                news_body=self.news_body,
                news_author=self.news_author,
                news_date=self.news_date,
                news_user_id=self.news_user_id
            )
            db.session.add(new_news)
            db.session.commit()
            db.session.refresh(new_news)
            new_news_id = new_news.id
            self.news_id = new_news_id

    def delete_news(self):
        with app.app_context():
            existing_news_list = News.query.filter_by(news_title=self.news_title).all()
            for news in existing_news_list:
                if news != None:
                    db.session.delete(news)
                    db.session.commit()

    def test_index_without_login(self):
        error_message = "test_index_without_login is failed."
        expected_response = b'Login'
        response = self.tester.get('/',
                               follow_redirects=True)
        self.assertEqual(response.status, '200 OK')
        self.assertIn(expected_response,response.data,error_message)

    def test_signup_with_valid_user(self):
        error_message = "test_signup_with_valid_user is failed."
        expected_response = b'Dashboard'
        response = self.tester.post('/signup',
                                    data=dict(
                                        email_address=self.email_address,
                                        password=self.password,
                                        repeat_password=self.password,
                                        full_name=self.full_name
                                    ),
                                    follow_redirects=True)
        self.assertEqual(response.status, '200 OK')
        self.assertIn(expected_response, response.data, error_message)

    def test_login_with_valid_user(self):
        error_message = 'test_login_with_valid_user is failed.'
        expected_response = b'Dashboard'
        user = self.recreate_user()
        response = self.tester.post('/login',
                                    data=dict(
                                        email_address=self.email_address,
                                        password=self.password
                                    ),
                                    follow_redirects=True)
        self.assertEqual(response.status, '200 OK')
        self.assertIn(expected_response, response.data, error_message)

    def test_login_with_invalid_user(self):
        error_message = "test_login_with_invalid_user is failed."
        expected_response = b'Sign in to start your session'
        response = self.tester.post('/login',
                                    data=dict(
                                        email_address=self.email_address,
                                        password=''),
                                    follow_redirects=True)
        self.assertEqual(response.status, '200 OK', "Error in response status")
        self.assertIn(expected_response, response.data, error_message)

    def test_show_news_with_invalid_id(self):
        error_message = "test_show_news_with_invalid_id is failed."
        expected_response = b'The news does not exist'
        response = self.tester.get('/news/88888/html',
                                    follow_redirects=True)
        self.assertEqual(response.status, '200 OK', "Error in response status")
        self.assertIn(expected_response, response.data, error_message)

    def test_show_news_with_invalid_format(self):
        error_message = "test_show_news_with_invalid_format is failed."
        expected_response1 = b'The news does not exist'
        expected_response2 = b'Unknown Format'
        response = self.tester.get('/news/1/fbml',
                                    follow_redirects=True)
        self.assertEqual(response.status, '200 OK', "Error in response status")
        self.assertIn(expected_response1, response.data, error_message) and \
        self.assertIn(expected_response2, response.data, error_message)


    def test_show_news_with_valid_id_html(self):
        error_message = "test_show_news_with_valid_id_html is failed."
        expected_response = bytes(self.news_title, encoding='utf-8')
        self.create_news()
        test_url = "/news/"+str(self.news_id)+"/html"
        response = self.tester.get(test_url,
                                    follow_redirects=True)
        self.assertEqual(response.status, '200 OK', "Error in response status")
        self.assertIn(expected_response, response.data, error_message)

    def test_show_news_with_valid_id_xml(self):
        error_message = "test_show_news_with_valid_id_xml is failed."
        expected_response = bytes(self.news_title, encoding='utf-8')
        self.create_news()
        test_url = "/news/"+str(self.news_id)+"/xml"
        response = self.tester.get(test_url,
                                    follow_redirects=True)
        self.assertEqual(response.status, '200 OK', "Error in response status")
        self.assertIn(expected_response, response.data, error_message)

    def test_show_news_with_valid_id_json(self):
        error_message = "test_show_news_with_valid_id_json is failed."
        expected_response = bytes(self.news_title, encoding='utf-8')
        self.create_news()
        test_url = "/news/"+str(self.news_id)+"/json"
        response = self.tester.get(test_url,
                                    follow_redirects=True)
        self.assertEqual(response.status, '200 OK', "Error in response status")
        self.assertIn(expected_response, response.data, error_message)

    def test_logout_without_login(self):
        response = self.tester.post('/logout',
                                    follow_redirects=True)
        self.assertEqual(response.status, '405 METHOD NOT ALLOWED', "Error in response status")

if __name__ == '__main__':
    unittest.main()
