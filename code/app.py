from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

# Resource are something that are api will return and in general Resources are mapped in database as well
# flask_restful internally handle return type jsonify. So we can directly return python dictionary
# next function give the first value and then next and next and so on

app = Flask(__name__)
app.secret_key = 'This is my secret key please don\'t share it '
api = Api(app)

jwt = JWT(app, authenticate, identity)  # This will add /auth in url

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


#It will prevent it from executing it when it is imported by some  other file. It will only execute when this file is executed
if __name__ == '__main__': 
    app.run(port=5000, debug=True)

