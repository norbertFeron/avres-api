from flask_restful import Resource, reqparse
from neo4j.v1 import ResultError
from connector import neo4j

parser = reqparse.RequestParser()


class CountAllPost(Resource):
    def get(self):
        req = "MATCH (:post) RETURN count(*) AS nb_posts"
        result = neo4j.query_neo4j(req)
        try:
            return result.single()['nb_posts'], 200
        except ResultError:
            return "ERROR", 500


class CountPostByAuthor(Resource):
    def get(self, author_id):
        req = "MATCH (author:user {uid : %d})-[:AUTHORSHIP]->(:post) RETURN count(*) AS nb_posts" % author_id
        result = neo4j.query_neo4j(req)
        try:
            return result.single()['nb_posts'], 200
        except ResultError:
            return "ERROR", 500