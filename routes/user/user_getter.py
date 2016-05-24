from flask_restful import Resource, reqparse
from neo4j.v1 import ResultError
from connector import neo4j

parser = reqparse.RequestParser()
parser.add_argument('limit')


class GetUserById(Resource):
    def get(self, user_id):
        result = neo4j.query_neo4j("MATCH (find:user {uid: %d}) RETURN find" % user_id)
        try:
            return result.single()['find'].properties, 200
        except ResultError:
            return "ERROR : Cannot find user with uid: %d" % user_id, 200  # todo create error code


class GetAllUsers(Resource):
    def get(self):
        req = "MATCH (find:user) RETURN find"
        args = parser.parse_args()
        if args['limit']:
            req += " LIMIT %s" % args['limit']
        result = neo4j.query_neo4j(req)
        users = []
        for record in result:
            users.append(record['find'].properties)
        return users


class GetShortestPathBetweenUsers(Resource):
    def get(self, user1_id, user2_id, max_hop):
        req = "MATCH path=shortestPath((u1:user {uid: %d})-[*..%d]-(u2:user {uid: %d}))RETURN path" % (
            user1_id, max_hop, user2_id)
        result = neo4j.query_neo4j(req)
        try:
            print(result.single()['path'])  # todo this is the path ?
            return 'I don\'t understand the result, sorry.', 200
        except ResultError:
            return "ERROR : Cannot find a path between uid: %d and uid: %d with maximum %d hop" % (
                user1_id, user2_id, max_hop), 200
