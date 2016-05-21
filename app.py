from flask import Flask
from flask_restful import Api
from routes.user.user_route import *

app = Flask(__name__)
api = Api(app)

#### USERS Routes ####
api.add_resource(GetAllUsers, '/users')
# ...
api.add_resource(GetUserById, '/user/id/<int:user_id>')
api.add_resource(GetUserByName, '/user/name/<string:user_name>')
# ...

if __name__ == '__main__':
    app.run(debug=True)
