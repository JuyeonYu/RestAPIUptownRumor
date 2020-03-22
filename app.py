from flask import Flask
from flask_restful import Api
from RestAPI import Post

app = Flask(__name__)
api = Api(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

api.add_resource(Post, '/post')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
