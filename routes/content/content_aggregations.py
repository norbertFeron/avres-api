from flask_restful import Resource, reqparse
from neo4j.v1 import ResultError
from connector import neo4j

parser = reqparse.RequestParser()


class CountAllContent(Resource):
    def get(self):
        req = "MATCH (:content) RETURN count(*) AS nb_contents"
        result = neo4j.query_neo4j(req)
        try:
            return result.single()['nb_contents'], 200
        except ResultError:
            return "ERROR", 500


class CountContentByAuthor(Resource):
    def get(self, author_id):
        req = "MATCH (author:user {uid : %d})-[:authorship]->(:content) RETURN count(*) AS nb_contents" % author_id
        print(req)
        result = neo4j.query_neo4j(req)
        try:
            return result.single()['nb_contents'], 200
        except ResultError:
            return "ERROR", 500