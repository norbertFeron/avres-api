from routes.user.user_getter import *


def add_user_routes(api):
    # Getters
    api.add_resource(GetUsers, '/users')
    api.add_resource(GetUserById, '/user/id/<int:user_id>')

    # Work in progress
    api.add_resource(GetShortestPathBetweenUsers, '/user/shortestPath/<int:user1_id>/<int:user2_id>/<int:max_hop>')

    # todo GetUserType
    # todo GetUsersByType moderators, ...