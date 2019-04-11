from app import db

class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    email_address = db.Column('email_address', db.String(150), index=True, unique=True)
    password = db.Column('password', db.String(150))
    full_name = db.Column('full_name', db.String(150))
    news = db.relationship("News", back_populates="user")

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.full_name)

class News(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    news_title = db.Column('news_title', db.String(150))
    news_body = db.Column('news_body', db.Text())
    news_author = db.Column('news_author', db.String(150))
    news_date = db.Column('news_date', db.Date())
    news_user_id = db.Column('news_user_id',
                             db.Integer,
                             db.ForeignKey('user.id'))
    user = db.relationship('User',
                            back_populates="news")
    def __repr__(self):
        return '<Post %r>' % (self.news_title)