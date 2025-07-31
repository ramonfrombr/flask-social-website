from flask import Flask, request, make_response, redirect, abort, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime, timezone

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'secret'

@app.route('/')
def index():
  return render_template('index.html', current_time=datetime.now(timezone.utc))

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