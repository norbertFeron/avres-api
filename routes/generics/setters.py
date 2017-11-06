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
        for key in request.get_json():
            for entry in request.get_json()[key]:
                if key == 'delete':
                    if 'pid' in entry.keys() and 'aid' in entry.keys() and entry['pid'] and entry['aid']:
                        query = "MATCH (n)--(l:Link:Prop)--(p:Property) WHERE ID(n) = %s AND ID(p) = %s WITH l MATCH (l)--(l2:Link:Attr)--(a) WHERE ID(a) = %s  DETACH DELETE l2" % (id, entry['pid'], entry['aid'])
                    elif 'pid' in entry.keys() and entry['pid']:
                        query = "MATCH (n)--(l:Link:Prop)--(p:Property) WHERE ID(n) = %s AND ID(p) = %s WITH l OPTIONAL MATCH (l)-[HAS]->(l2:Link) DETACH DELETE l, l2" % (id, entry['pid'])
                    neo4j.query_neo4j(query)
                    break
                if key == 'create':
                    if 'aid' in entry.keys():
                        query = "MATCH (n)--(l:Link:Prop)--(p:Property) WHERE ID(n) = %s AND ID(p) = %s MATCH (a:Attribute) WHERE ID(a) = %s  MERGE (l)-[:HAS]->(:Link:Attr)-[:IS]->(a)" % (id, entry['pid'], entry['aid'])
                        neo4j.query_neo4j(query)
                    break
                if 'pid' in entry.keys():
                    query = "MATCH (p:Property:%s) WHERE ID(p) = %s RETURN p.value as value" % (key, entry['pid'])
                    if neo4j.query_neo4j(query).single()['value'] != entry['value']:
                        query = "MATCH (n)--(l:Link:Prop)--(p:Property:%s) WHERE ID(n) = %s AND ID(p) = %s WITH l OPTIONAL MATCH (l)-[HAS]->(l2:Link) DETACH DELETE l, l2" % (key, id, entry['pid'])
                        neo4j.query_neo4j(query)
                        query = "MERGE (p:Property:%s {value: '%s'}) WITH p MATCH (n) WHERE ID(n) = %s" % (key, entry['value'], id)
                        query += " WITH p, n MERGE (n)-[:HAS]->(:Link:Prop)-[:IS]->(p)"
                if 'pid' not in entry.keys():
                    query = "MERGE (p:Property:%s {value: '%s'}) WITH p MATCH (n) WHERE ID(n) = %s" % (key, entry['value'], id)
                    query += " WITH p, n MERGE (n)-[:HAS]->(:Link:Prop)-[:IS]->(p)"
                neo4j.query_neo4j(query)
        return makeResponse('maybe ok', 200) # todo: manage error code and exception


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
        index = 0
        for key in request.get_json():
            if not key == 'id':
                query += ' MERGE (%s:Property:%s {value: "%s"})' % ('a' + str(index), key, request.get_json()[key])
                query += ' WITH * MERGE (n)-[:HAS]->(:Link:Prop)-[:IS]->(%s)' % ('a' + str(index))
                index += 1
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
          @apiDescription Link two nodes with an edges
          @apiSuccess ok
       """
        edge = request.get_json()
        query = "MATCH (edge) WHERE ID(edge) = %s RETURN labels(edge) as labels" % edge['id']
        result = neo4j.query_neo4j(query).single()
        query = "MATCH (source) WHERE ID(source) = %s" % edge['source']
        query += " WITH source MATCH (target) WHERE ID(target) = %s" % edge['target']
        query += " WITH source, target MATCH (edge) WHERE ID(edge) = %s" % edge['id']
        if 'Attr' in result['labels']:
            query += " WITH source, target, edge CREATE r=(source)-[:HAS]->(edge)-[:IS]->(target) RETURN r"
        elif 'Prop' in result['labels']:
            query += " WITH source, target, edge CREATE r=(source)-[:HAS]->(edge)-[:IS]->(target) RETURN r"
        else:
            query += " WITH source, target, edge CREATE r=(source)-[:LINK]->(edge)-[:LINK]->(target) RETURN r"
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
        query = "MATCH (n)--(pl:Prop)--(p:Property) WHERE ID(n) = %s DETACH DELETE n, pl RETURN ID(p) as prop" % id
        result = neo4j.query_neo4j(query)
        for record in result:
            query = "MATCH (p:Property) WHERE id(p) = %s AND NOT (p)--() DETACH DELETE p" % record['prop']
            neo4j.query_neo4j(query)
        try:
            return makeResponse('Deleted', 200) # todo: error managing
        except ResultError:
            return makeResponse("Unable to delete node", 400)