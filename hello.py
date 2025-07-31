from flask import Flask, request

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

if __name__ == '__main__':
  app.run()