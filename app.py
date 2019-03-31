from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #sqlalachemy is going to read data.db we already created
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)  # jwt creates a new endpoint /auth
"""
when we call /auth , we send it a username and a password, the jwt extesnion gets
the username and password and sends it over to the "authenticate" function (see security.py),
that takes in a username and a password (if username and pwd (compare the
pwd with the one that we received through the auth endpoint) match, we are then going to return the user),
the auth endpoint returns a JW token - that JWtoken doesn't do anything, but we can send it to the ext request
-when we send a JW token, what jw does is calls the "identity" function and then uses the JWtoken to get the user
id - and with that it gets the correct user id that the JW token represents
"""

api.add_resource(Store, '/store/<string:name>')

# http://127.0.0.1:5000/item/
api.add_resource(Item, '/item/<string:name>')

# make sure to give the correct endpoint for itemList
api.add_resource(ItemList, "/items")

api.add_resource(StoreList, '/stores')
# add the UserRegister resource as an endpoint, so that when we execute a POST request
# to /register that's gonna call UserRegister and going to call the Post method
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
