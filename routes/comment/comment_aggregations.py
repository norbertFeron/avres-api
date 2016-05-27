from flask_restful import Resource, reqparse
from neo4j.v1 import ResultError
from connector import neo4j

parser = reqparse.RequestParser()


class CountAllComments(Resource):
    def get(self):
        req = "MATCH (:comment) RETURN count(*) AS nb_comments"
        result = neo4j.query_neo4j(req)
        try:
            return result.single()['nb_comments'], 200
        except ResultError:
            return "ERROR", 500


class CountCommentsByAuthor(Resource):
    def get(self, author_id):
        req = "MATCH (author:user {uid : %d})-[:AUTHORSHIP]->(c:comment) RETURN count(*) AS nb_comments" % author_id
        result = neo4j.query_neo4j(req)
        try:
            return result.single()['nb_comments'], 200
        except ResultError:
            return "ERROR", 500

