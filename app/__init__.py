from flask import Flask, make_response, redirect, abort, render_template, session, url_for
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(config[config_name])
  config[config_name].init_app(app)

  bootstrap.init_app(app)
  mail.init_app(app)
  moment.init_app(app)
  db.init_app(app)

  from .email import send_email
  from .models import User, Role

  class NameForm(FlaskForm):
    name = StringField('What is your name?',  validators=[DataRequired()])
    submit = SubmitField('Submit')

  @app.route('/', methods=['GET', 'POST'])
  def index():
    form = NameForm()
    if form.validate_on_submit():
      user = User.query.filter_by(username=form.name.data).first()
      if user is None:
        user = User(username=form.name.data)
        db.session.add(user)
        db.session.commit()
        session['known'] = False
        if app.config['APP_ADMIN']:
          send_email(app.config['APP_ADMIN'], 'New User', 'mail/new_user', user=user)
      else:
        session['known'] = True
      session['name'] = form.name.data
      form.name.data = ''
      return redirect(url_for('index'))
    return render_template(
      'index.html',
      form=form,
      name=session.get('name'),
      known=session.get('known', False),
      current_time=datetime.now(timezone.utc)
    )

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

  @app.shell_context_processor
  def make_shell_context():
    return dict(db=db, User=User, Role=Role)

  return app