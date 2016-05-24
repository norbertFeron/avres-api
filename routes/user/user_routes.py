from routes.user.user_getter import *


def add_user_routes(api):
    # Getters
    api.add_resource(GetAllUsers, '/users')
    api.add_resource(GetUserById, '/user/id/<int:user_id>')