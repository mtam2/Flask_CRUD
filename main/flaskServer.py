from flask import Flask, flash, g, redirect, render_template, request, session, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
import os

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.path.join(app.root_path, 'ahoy.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ahoy.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = pwd_context.hash(password)


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Purpose:
        Displays login form if logged_in cookie does not exist and
        redirects to landing page if it does exist.
    Args:
        None.
    Returns:
        Renders home.html or redirects to landing.html if logged in.
    """
    if request.method == 'POST':
        if not request.form['username'] or not request.form['password']:
            return render_template('home.html', invalid_input=True)
        else:
            # Verifies existing user and valid hashed password
            user_query = User.query.filter_by(
                username=request.form['username']).first()
            if user_query is None:
                return render_template('home.html', invalid_user=True)
            else:
                is_valid = pwd_context.verify(
                    request.form['password'], user_query.password)
                current_username = request.form['username']
                if is_valid:
                    session['logged_in'] = True
                    session['username'] = current_username
                    return redirect(url_for('landing'))
                else:
                    return render_template('home.html', invalid_user=True)
    if 'logged_in' in session:
        if session['logged_in']:
            return redirect(url_for('landing'))
    return render_template('home.html')


@app.route('/landing')
def landing():
    return render_template('landing.html')


@app.route('/create', methods=['GET', 'POST'])
def create():
    """
    Purpose:
        Displays create form for user.
    Args:
        None.
    Returns:
        Renders create.html. If username already exists,
        page prompts username already exists text.
    """
    if request.method == 'POST':
        if not request.form['username'] or not request.form['password']:
            return render_template('create.html', invalid_input=True)
        else:
            user_query = User.query.filter_by(
                username=request.form['username']).count()
            if user_query > 0:
                return render_template('create.html', invalid_username=True)
            else:
                temp_user = User(
                    request.form['username'], request.form['password'])
                db.session.add(temp_user)
                db.session.commit()
                return render_template('create.html', successful=True)
    return render_template('create.html')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.clear()
    return render_template('home.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=8080)
