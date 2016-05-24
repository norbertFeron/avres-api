from flask_restful import Resource, reqparse
from neo4j.v1 import ResultError
from connector import neo4j

parser = reqparse.RequestParser()
parser.add_argument('limit')


class GetUserById(Resource):
    def get(self, user_id):
        result = neo4j.uery_neo4j("MATCH (find:user {uid: %d}) RETURN find" % user_id)
        try:
            return result.single()['find'].properties, 200
        except ResultError:
            return "ERROR : Cannot find user with uid: %d" % user_id, 200  # todo create error code


class GetUserByName(Resource):
    def get(self, user_name):
        result = neo4j.query_neo4j("MATCH (find:user {name: '%s'}) RETURN find" % user_name)
        try:
            return result.single()['find'].properties, 200
        except ResultError:
            return "ERROR : Cannot find user with name: %d" % user_name, 200


class GetAllUsers(Resource):
    def get(self):
        req = "MATCH (find:user) RETURN find"
        args = parser.parse_args()
        if args['limit']:
            req = req + " LIMIT %s" % args['limit']
        result = neo4j.query_neo4j(req)
        users = []
        for record in result:
            users.append(record['find'].properties)
        return users