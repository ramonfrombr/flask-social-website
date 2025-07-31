from flask import Flask, request, make_response

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

if __name__ == '__main__':
  app.run()