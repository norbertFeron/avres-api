from flask_restful import Resource, reqparse
from neo4j.v1 import ResultError
from connector import neo4j
from routes.utils import arglimit

parser = reqparse.RequestParser()


class GetContentById(Resource):
    def get(self, content_id):
        result = neo4j.query_neo4j("MATCH (find:content {nid: %d}) RETURN find" % content_id)
        try:
            return result.single()['find'].properties, 200
        except ResultError:
            return "ERROR : Cannot find content with nid: %d" % content_id, 200


class GetAllContents(Resource):
    def get(self):
        req = "MATCH (find:content) RETURN find"
        req += arglimit()
        result = neo4j.query_neo4j(req)
        contents = []
        for record in result:
            contents.append(record['find'].properties)
        return contents


class GetAllContentsByType(Resource):
    def get(self, content_type):
        req = "MATCH (find:content {type: '%s'}) RETURN find" % content_type
        req += arglimit()
        result = neo4j.query_neo4j(req)
        contents = []
        for record in result:
            contents.append(record['find'].properties)
        return contents


class GetAllContentsByAuthor(Resource):
    def get(self, author_id):
        req = "MATCH (author:user {uid: %d})-[:authorship]->(c:content) RETURN c" % author_id
        req += arglimit()
        result = neo4j.query_neo4j(req)
        contents = []
        for record in result:
            contents.append(record['c'].properties)
        return contents


class GetContentType(Resource):
    def get(self):
        req = "MATCH (c:content) WHERE EXISTS(c.type) RETURN DISTINCT c.type AS type"
        result = neo4j.query_neo4j(req)
        types = []
        for record in result:
            types.append(record['type'])
        return types
