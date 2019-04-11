from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, DateField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class author_login_form(FlaskForm):
    email_address = StringField('email_address', validators=[DataRequired(message='Email is required'),Email()])
    password = PasswordField('password', validators=[DataRequired(message='Password is required')])

class author_signup_form(FlaskForm):
    email_address = StringField('email_address', validators=[DataRequired(message='Email is required'),Email()])
    password = PasswordField('password',
                             validators=[DataRequired(message='Password is required'),
                                         EqualTo('repeat_password', message='Passwords must match'),
                                         Length(min=6,message='Password minimum length is 6')])
    repeat_password = PasswordField('repeat_password',
                                    validators=[DataRequired(message='Repeating password is required')])
    full_name = StringField('full_name', validators=[DataRequired(message=' is required')])

class add_news_form(FlaskForm):
    news_title = StringField('news_title', validators=[DataRequired(message='Title is required')])
    news_body = TextAreaField('news_body', validators=[DataRequired(message='Body is required')])
    news_author = StringField('news_author', validators=[DataRequired(message='Author is required')])
    news_date = DateField('news_date', validators=[DataRequired(message='Date is required')])
