from flask_restful import Resource, reqparse
from neo4j.v1 import ResultError
from connector import neo4j

parser = reqparse.RequestParser()
parser.add_argument('drawing')
parser.add_argument('limit')


class GetCommentById(Resource):
    def get(self, comment_id):
        result = neo4j.query_neo4j("MATCH (find:comment {cid: %d}) RETURN find" % comment_id)
        try:
            return result.single()['find'].properties, 200
        except ResultError:
            return "ERROR : Cannot find comment with cid: %d" % comment_id, 200  # todo create error code


class GetCommentByTitle(Resource):
    def get(self, comment_title):
        result = neo4j.query_neo4j("MATCH (find:comment {title: '%s'}) RETURN find" % comment_title)
        try:
            return result.single()['find'].properties, 200
        except ResultError:
            return "ERROR : Cannot find comment with id: %d" % comment_title, 200


class GetAllComments(Resource):
    def get(self):
        req = "MATCH (find:comment) RETURN find"
        args = parser.parse_args()
        if args['limit']:
            req = req + " LIMIT %s" % args['limit']
        result = neo4j.query_neo4j(req)
        comments = []
        for record in result:
            comments.append(record['find'].properties)
        return comments


class GetAllCommentsBetweenUsers(Resource):
    def get(self, user1, user2):
        req = ""
        args = parser.parse_args()
        if args['limit']:
            req = req + " LIMIT %s" % args['limit']
        result = neo4j.query_neo4j(req)
        comments = []
        for record in result:
            comments.append(record['find'].properties)
        return comments
