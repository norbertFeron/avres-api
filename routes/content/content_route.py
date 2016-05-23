from flask_restful import Resource, reqparse, abort
from neo4j.v1 import ResultError
from connector import neo4j

parser = reqparse.RequestParser()
parser.add_argument('drawing')
parser.add_argument('limit')


class GetContentById(Resource):
    def get(self, content_id):
        result = neo4j.query_neo4j("MATCH (find:content {nid: %d}) RETURN find" % content_id)
        try:
            return result.single()['find'].properties, 200
        except ResultError:
            return "ERROR : Cannot find content with nid: %d" % content_id, 200  # todo create error code


class GetContentByTitle(Resource):
    def get(self, content_title):
        result = neo4j.query_neo4j("MATCH (find:content {title: '%s'}) RETURN find" % content_title)
        try:
            return result.single()['find'].properties, 200
        except ResultError:
            return "ERROR : Cannot find content with id: %d" % content_title, 200


class GetAllContents(Resource):
    def get(self):
        req = "MATCH (find:content) RETURN find"
        args = parser.parse_args()
        if args['limit']:
            req += " LIMIT %s" % args['limit']
        result = neo4j.query_neo4j(req)
        contents = []
        for record in result:
            contents.append(record['find'].properties)
        return contents


class GetAllContentsByType(Resource):
    def get(self, content_type):
        req = "MATCH (find:content {type: '%s'}) RETURN find" % content_type
        args = parser.parse_args()
        if args['limit']:
            req += " LIMIT %s" % args['limit']
        result = neo4j.query_neo4j(req)
        contents = []
        for record in result:
            contents.append(record['find'].properties)
        return contents
