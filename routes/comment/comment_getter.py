from flask_restful import Resource
from neo4j.v1 import ResultError
from connector import neo4j
from routes.utils import addargs


class GetComment(Resource):
    def get(self, comment_id):
        result = neo4j.query_neo4j("MATCH (find:comment {cid: %d}) RETURN find" % comment_id)
        try:
            return result.single()['find'].properties, 200
        except ResultError:
            return "ERROR : Cannot find comment with cid: %d" % comment_id, 200


class GetCommentHydrate(Resource):
    def get(self, comment_id):
        req = "MATCH (find:comment {cid: %d})<-[:authorship]-(author:user)" % comment_id
        req += "RETURN find, author"
        result = neo4j.query_neo4j(req)
        try:
            record = result.single()
            comment = record['find'].properties
            comment['author'] = record['author'].properties
            return comment, 200
        except ResultError:
            return "ERROR : Cannot find comment with cid: %d" % comment_id, 200


class GetComments(Resource):
    def get(self):
        req = "MATCH (find:comment) RETURN find"
        req += addargs()
        result = neo4j.query_neo4j(req)
        comments = []
        for record in result:
            comments.append(record['find'].properties)
        return comments


class GetCommentsByAuthor(Resource):
    def get(self, author_id):
        req = "MATCH (author:user {uid: %d})-[:authorship]->(c:comment) RETURN c" % author_id
        req += addargs()
        result = neo4j.query_neo4j(req)
        comments = []
        for record in result:
            comments.append(record['c'].properties)
        return comments


class GetCommentsOnContent(Resource):
    def get(self, content_id):
        req = "MATCH (c:comment)-[:comments]->(content:content { nid: %d}) RETURN c" % content_id # todo restructure maybe change nid
        req += addargs()
        result = neo4j.query_neo4j(req)
        comments = []
        for record in result:
            comments.append(record['c'].properties)
        return comments


class GetCommentsOnComment(Resource):
    def get(self, comment_id):
        req = "MATCH (c:comment)-[:comments]->(comment:comment { cid: %d}) RETURN c" % comment_id
        req += addargs()
        result = neo4j.query_neo4j(req)
        comments = []
        for record in result:
            comments.append(record['c'].properties)
        return comments
