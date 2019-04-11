WTF_CSRF_ENABLED = True
SECRET_KEY = 'j233hs@#d@dsz65a'
JSON_SORT_KEYS = False
import os
basedir = os.path.abspath(os.path.dirname(__file__))

#mysql://username:password@localhost/database_name
SQLALCHEMY_DATABASE_URI = 'mysql://newsroom_db_admin:newsroom_db_password@localhost/newsroom_db'

#'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# pagination
POSTS_PER_PAGE = 5