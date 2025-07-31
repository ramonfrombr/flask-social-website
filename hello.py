from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
  user_agent = request.headers.get('User-Agent')
  return '<h1>Hello World! You browser is {}</h1>'.format(user_agent)

@app.route('/user/<name>')
def user(name):
  return '<h1>Hello, {}!'.format(name)

if __name__ == '__main__':
  app.run()