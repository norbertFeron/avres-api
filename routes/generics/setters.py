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
          @apiParam {String} id id
          @apiSuccess {String} id of the node
       """
        query = "MATCH (n) WHERE ID(n) = %s" % id
        for key in request.get_json():
            if not key == 'id':
                query += " SET n.%s = '%s'" % (key, request.get_json()[key])
        query += " RETURN ID(n) as id"
        result = neo4j.query_neo4j(query)
        try:
            return makeResponse(result.single()['id'], 200)
        except ResultError:
            return makeResponse("Unable to find id: %s" % id, 400)


class CreateNode(Resource):
    def post(self):
        """
          @api {post} /createNode/ Create new node
          @apiName create
          @apiGroup Setters
          @apiDescription create a node
          @apiSuccess {String} id of the node
       """
        node = request.get_json()
        labels = node['labels']
        del node['labels']
        query = "CREATE (n:"
        for l in labels:
            query += "%s:" % l
        query = "%s) " % query[:-1]
        for key in request.get_json():
            if not key == 'id':
                query += " SET n.%s = '%s'" % (key, request.get_json()[key])
        query += " RETURN ID(n) as id"
        result = neo4j.query_neo4j(query)
        try:
            return makeResponse(result.single()['id'], 200)
        except ResultError:
            return makeResponse("Unable to create a new node", 400)


class CreateEdge(Resource):
    def post(self):
        """
          @api {post} /createEdge/ Create new edge
          @apiName create
          @apiGroup Setters
          @apiDescription create a node
          @apiSuccess {String} id of the node
       """
        edge = request.get_json()
        query = "MATCH (source) WHERE ID(source) = %s" % edge['source']
        query += " WITH source MATCH (target) WHERE ID(target) = %s" % edge['target']
        query += " WITH source, target MATCH (edge) WHERE ID(edge) = %s" % edge['id']
        query += " WITH source, target, edge CREATE r=(source)-[:HAS]->(edge)-[:HAS]->(target) RETURN r"
        result = neo4j.query_neo4j(query)
        try:
            return makeResponse("ok", 200)
        except ResultError:
            return makeResponse("Unable to create a new edge", 400)


class DeleteById(Resource):
    def delete(self, id):
        """
          @api {delete} /:id
          @apiName delete
          @apiGroup Setters
          @apiDescription delete a node
       """
        query = "MATCH (n) WHERE ID(n) = %s DETACH DELETE n" % id
        result = neo4j.query_neo4j(query)
        try:
            return makeResponse('Deleted', 200) # todo: error managing
        except ResultError:
            return makeResponse("Unable to delete node", 400)