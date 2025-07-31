from flask import Flask, request, make_response, redirect, abort

app = Flask(__name__)

@app.route('/')
def index():
  user_agent = request.headers.get('User-Agent')
  return '<h1>Hello World! You browser is {}</h1>'.format(user_agent)

@app.route('/user/<name>')
def user(name):
  return '<h1>Hello, {}!'.format(name)

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

if __name__ == '__main__':
  app.run()