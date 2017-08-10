from neo4j.v1 import ResultError

from connector import neo4j
from flask_restful import Resource, reqparse
from routes.utils import makeResponse, addargs

parser = reqparse.RequestParser()


class CountLabel(Resource):
    """
      @api {get} /countLabel/:label Count iteration of a label
      @apiName CountLabels
      @apiGroup Counters
      @apiDescription Return number of iteration for a label
      @apiParam {String} label Label
      @apiSuccess {Integer} result nb of iteration for the label
   """
    def get(self, label):
        query = "MATCH (n:%s) RETURN COUNT(n) as iteration" % label
        result = neo4j.query_neo4j(query)
        return makeResponse(result.single()['iteration'], 200)