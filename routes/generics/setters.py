from neo4j.v1 import ResultError

from connector import neo4j
from flask_restful import Resource, reqparse, request
from routes.utils import makeResponse

parser = reqparse.RequestParser()
parser.add_argument('keys', action='append')
parser.add_argument('filters', action='append')


class SetById(Resource):
    def put(self, id):
        """
          @api {put} /set/:id Set by id 
          @apiName SetById
          @apiGroup Setters
          @apiDescription Modify a node
          @apiParam {String} label Label
          @apiSuccess {String} id of the node
       """
        query = "MATCH (n) WHERE ID(n) = %s" % id
        for key in request.form.keys():
            query += " SET n.%s = '%s'" % (key, request.form[key])
        query += " RETURN ID(n) as id"
        result = neo4j.query_neo4j(query)
        try:
            return makeResponse(result.single()['id'], 200)
        except ResultError:
            return makeResponse("Unable to find id: %s" % id, 400)
