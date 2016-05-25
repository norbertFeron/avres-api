from flask_restful import Resource
from neo4j.v1 import ResultError
from connector import neo4j
from routes.utils import addargs


class GetContent(Resource):
    def get(self, content_id):
        result = neo4j.query_neo4j("MATCH (find:content {nid: %d}) RETURN find" % content_id)
        try:
            return result.single()['find'].properties, 200
        except ResultError:
            return "ERROR : Cannot find content with nid: %d" % content_id, 200


class GetContentHydrate(Resource): # todo comments on comments (with author)
    def get(self, content_id):
        req = "MATCH (find:content {nid: %d})<-[:authorship]-(author:user)" % content_id
        req += "MATCH (find)<-[:comments]-(comment:comsment)<-[:authorship]-(commentAuthor:user)"
        req += "RETURN find, author, comment, commentAuthor"
        result = neo4j.query_neo4j(req)
        comments = []
        for record in result:
            user = record['find'].properties
            if record['author']:
                author = record['author'].properties
            if record['comment']:
                comment = record['comment'].properties
                if record['commentAuthor']:
                    comment['author'] = record['commentAuthor'].properties
                comments.append(comment)
        user['comments'] = comments
        user['author'] = author
        return user, 200


class GetContents(Resource):
    def get(self):
        req = "MATCH (find:content) RETURN find"
        req += addargs()
        result = neo4j.query_neo4j(req)
        contents = []
        for record in result:
            contents.append(record['find'].properties)
        return contents


class GetContentsByType(Resource):
    def get(self, content_type):
        req = "MATCH (find:content {type: '%s'}) RETURN find" % content_type
        req += addargs()
        result = neo4j.query_neo4j(req)
        contents = []
        for record in result:
            contents.append(record['find'].properties)
        return contents


class GetContentsByAuthor(Resource):
    def get(self, author_id):
        req = "MATCH (author:user {uid: %d})-[:authorship]->(c:content) RETURN c" % author_id
        req += addargs()
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
