from neo4j.v1 import ResultError

from connector import neo4j
from flask_restful import Resource, reqparse
from routes.utils import makeResponse, addargs

parser = reqparse.RequestParser()


class CountLabel(Resource):
    """
      @api {get} /countLabel/:label Count iteration of a label
      @apiName CountLabel
      @apiGroup Counters
      @apiDescription Return number of iteration for a label
      @apiParam {String} label Label
      @apiSuccess {Integer} result nb of iteration for the label
   """
    def get(self, label):
        query = "MATCH (n:%s) RETURN COUNT(n) as iteration" % label
        result = neo4j.query_neo4j(query)
        return makeResponse(result.single()['iteration'], 200)


class CountLabels(Resource):
    """
      @api {get} /countLabels/ Count iteration of all labels
      @apiName CountLabels
      @apiGroup Counters
      @apiDescription Return number of iteration for all labels
      @apiSuccess {Integer} Array of labels with nb of iteration
   """
    def get(self):
        query = "MATCH (a) WITH DISTINCT LABELS(a) AS temp, COUNT(a) AS tempCnt UNWIND temp AS label RETURN label, SUM(tempCnt) AS cnt"
        result = neo4j.query_neo4j(query)
        labels = {}
        for record in result:
            labels[record['label']] = record['cnt']
        return makeResponse(labels, 200)
