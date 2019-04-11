import hashlib
from flask import render_template, flash, redirect, request, url_for, g, Markup, escape
from flask import Response, jsonify, make_response
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from .forms import author_login_form
from .forms import author_signup_form
from .forms import add_news_form
from .models import User, News
from config import POSTS_PER_PAGE
import json
import site_information

information = site_information.information


def get_hashed_password(user_password):
    salt = "cefalologin"
    salted_password = user_password + salt
    hashed_value = hashlib.md5(salted_password.encode())
    return hashed_value.hexdigest()


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user

@app.errorhandler(403)
def not_found_error(error):
    information["site_title"] = "Forbidden"
    information["page_header"] = "Error 403 - Forbidden"
    information["page_description"] = ""
    error_code = 403
    error_message = "Sorry, access denied or forbidden!"
    return render_template('4xx.html',
                           information = information,
                           error_code = error_code,
                           error_message=error_message), 403


@app.errorhandler(404)
def not_found_error(error):
    information["site_title"] = "File not found"
    information["page_header"] = "Error 404 - File not found"
    information["page_description"] = ""
    error_code = 404
    error_message = "Sorry, requested page is not found!"
    return render_template('4xx.html',
                           information = information,
                           error_code = error_code,
                           error_message=error_message), 404

@app.errorhandler(405)
def not_allowed_error(error):
    information["site_title"] = "Method not allowed"
    information["page_header"] = "Error 405 - Method not allowed"
    information["page_description"] = ""
    error_code = 405
    error_message = "Sorry, this method is not allowed!"
    return render_template('4xx.html',
                           information = information,
                           error_code = error_code,
                           error_message = error_message), 405

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    information["site_title"] = "Error"
    information["page_header"] = "Error"
    information["page_description"] = "Error 500"
    return render_template('500.html', information=information), 500


@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page=1):
    information["site_title"] = "Dashboard"
    information["page_header"] = "Dashboard"
    information["page_description"] = ""
    # news_list = News.query.order_by("id desc").all()
    news_list = News.query.order_by("id desc").paginate(page, POSTS_PER_PAGE, False)
    count_user = len(User.query.all())
    count_news = len(News.query.all())

    return render_template(
        'home.html', information=information,
        news_list=news_list,
        count_user=count_user,
        count_news=count_news
    )


@app.route('/news/<int:news_id>/<string:response_format>')
def show_news(news_id, response_format):
    information["site_title"] = "News Details"
    information["page_header"] = "News Details"
    information["page_description"] = ""
    news_details = News.query.filter_by(id=news_id).first()
    if news_details == None:
        flash("The news does not exist")
        return redirect(url_for('index'))
    else:
        news = {}
        news["id"] = news_details.id
        news["title"] = news_details.news_title
        news["body"] = news_details.news_body
        news["author"] = news_details.news_author
        news["date"] = news_details.news_date
        if response_format.lower() == "html":
            news_details.news_body = Markup(news_details.news_body)
            return render_template(
                'news.html', information=information,
                news_details=news_details
            )
        elif response_format.lower() == "json":
            return jsonify(news)
        elif response_format.lower() == "xml":
            response = make_response(render_template('single_news.xml', news=news))
            response.headers["Content-Type"] = "text/xml; charset=utf-8"
            return response
        else:
            flash("Unknown Format")
            return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    information["site_title"] = "Login"
    information["page_header"] = "Login Page"
    information["page_description"] = "Showing Login Form"
    form = author_login_form()
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == "GET":
        return render_template('login.html', form=form, information=information)
    else:
        if form.validate_on_submit():
            email_address = form.email_address.data
            password = get_hashed_password(form.password.data)
            existing_user = User.query.filter_by(email_address=email_address).first()
            if existing_user == None:
                flash('Email address %s is not registered.' %
                      (email_address))
                return redirect(url_for('login'))
            else:
                if existing_user.password == password:
                    login_user(existing_user, remember=True)
                    return redirect(request.args.get('next') or url_for('index'))
                else:
                    flash("Password is incorrect")
                    return redirect(url_for('login'))
        else:
            flash("Form validation failed")
            return render_template('login.html', form=form, information=information)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    information["site_title"] = "Signup"
    information["page_header"] = "Signup Page"
    information["page_description"] = "Showing Signup Form"
    form = author_signup_form()
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == "GET":
        return render_template('registration.html',
                               form=form, information=information)
    else:
        if form.validate_on_submit():
            email_address = form.email_address.data
            password = get_hashed_password(form.password.data)
            full_name = form.full_name.data
            existing_user = User.query.filter_by(email_address=email_address).first()
            if existing_user == None:
                new_user = User(email_address=email_address, password=password, full_name=full_name)
                db.session.add(new_user)
                db.session.commit()
                flash('Welcome %s' % full_name)
                login_user(new_user)
                return redirect(url_for('index'))
            else:
                flash("An user existed using the " + email_address)
                return redirect(url_for('signup'))
        else:
            flash("Form validation failed")
            return render_template('registration.html',
                                   form=form, information=information)


@app.route('/add_news', methods=['GET', 'POST'])
@login_required
def add_news():
    information["site_title"] = "Add News"
    information["page_header"] = "Add News Page"
    information["page_description"] = "Showing Add News Form"
    form = add_news_form()

    if request.method == "GET":
        return render_template('add_edit_news.html',
                               form=form, information=information)
    else:
        if form.validate_on_submit():
            news_title = escape(form.news_title.data)
            news_body = escape(form.news_body.data)
            news_author = escape(form.news_author.data)
            news_date = escape(form.news_date.data)
            news_user_id = current_user.id
            new_news = News(news_title=news_title, news_body=news_body,
                            news_author=news_author, news_date=news_date, news_user_id=news_user_id)
            db.session.add(new_news)
            db.session.commit()
            flash('Created news %s' % news_title)
            return redirect(url_for('add_news'))
        else:
            flash("Form validation failed")
            return render_template('add_edit_news.html',
                                   form=form, information=information)

@app.route('/edit_news/<int:news_id>', methods=['GET', 'POST'])
@login_required
def edit_news(news_id):
    information["site_title"] = "Edit News"
    information["page_header"] = "Edit News"
    information["page_description"] = ""
    referrer = str(request.referrer)
    news = News.query.filter_by(id=news_id).first()
    if news == None:
        flash("The news does not exist")
        return redirect(referrer)
    else:
        if current_user.id!= news.news_user_id:
            flash("You are not authorised to edit this")
            return redirect(url_for('index'))
        form = add_news_form(obj=news)
        if request.method == "GET":
            return render_template('add_edit_news.html',
                                   form=form, information=information, news=news)
        else:
            if form.validate_on_submit():
                news.news_title = escape(form.news_title.data)
                news.news_body = escape(form.news_body.data)
                news.news_author = escape(form.news_author.data)
                news.news_date = escape(form.news_date.data)
                news.news_user_id = current_user.id
                db.session.commit()
                flash('Updated news %s' % news.news_title)
                return redirect(referrer)
            else:
                flash("Form validation failed")
                return render_template('add_edit_news.html',
                                       form=form, information=information, news=news)


@app.route('/delete_news', methods=['POST'])
@login_required
def delete_news():
    referrer = str(request.referrer)
    if request.method == "POST":
        news_id = request.form.get('delete_news_id')
        existing_news = News.query.get(news_id)
        if existing_news != None:
            if current_user.id != existing_news.news_user_id:
                flash("You are not authorised to delete this")
                return redirect(url_for('index'))
            flash("Deleted: "+existing_news.news_title)
            db.session.delete(existing_news)
            db.session.commit()
            return redirect(referrer)
        else:
            flash("News not found")
            return redirect(referrer)
    else:
        flash("Invalid Request")
        return redirect(referrer)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out.')
    return redirect(url_for('index'))
