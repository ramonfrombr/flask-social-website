import os
from flask import Flask, request, make_response, redirect, abort, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime, timezone
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Role(db.Model):
  __tablename__ = 'roles'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), unique=True)

  users = db.relationship('User', backref='role')

  def __repr__(self):
    return '<Role %r>' % self.name

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), unique=True, index=True)

  role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

  def __repr__(self):
    return '<User %r>' % self.username

class NameForm(FlaskForm):
  name = StringField('What is your name?',  validators=[DataRequired()])
  submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
  form = NameForm()
  if form.validate_on_submit():
    old_name = session.get('name')
    if old_name is not None and old_name != form.name.data:
      flash("Looks like you have changed your name!")
    session['name'] = form.name.data
    return redirect(url_for('index'))
  return render_template('index.html', form=form, name=session.get('name'), current_time=datetime.now(timezone.utc))

@app.route('/user/<name>')
def user(name):
  return render_template('user.html', name=name)

@app.route('/bad_request')
def bad_request():
  return '<h1>Bad Request</h1>', 400

@app.route('/make_response')
def make_response_route():
  response = make_response('<h1>This document carries a cookie!</h1>')
  response.set_cookie('answer', '42')
  return response

@app.route('/redirect_to_home')
def redirect_to_home():
  return redirect('/')

@app.route('/odd_numbers/<int:number>')
def odd_numbers(number):
  list_of_numbers = [1, 3, 5, 7, 9]
  if number not in list_of_numbers:
    abort(404)
  return '<h1>The number {} is included in {}.</h1>'.format(number, list_of_numbers)

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
  return render_template('500.html'), 500

if __name__ == '__main__':
  app.run()