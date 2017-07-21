from connector import neo4j
from flask_restful import Resource
from routes.utils import makeResponse


class GetPropertiesByLabel(Resource):
    def get(self, label):
        query = "MATCH (n:%s) WITH n UNWIND keys(n) as k RETURN COLLECT(DISTINCT k) as keys" % label
        result = neo4j.query_neo4j(query)
        return makeResponse(result.single()['keys'], 200)


class GetPropertyValueByLabel(Resource):
    def get(self, label, key):
        query = "MATCH (n:%s) RETURN COLLECT(DISTINCT n.%s) as values" % (label, key)
        result = neo4j.query_neo4j(query)
        return makeResponse(result.single()['values'], 200)


class GetByLabel(Resource):
    def get(self, label):
        return makeResponse('todo', 200)


class GetByLabelAndId(Resource):
    def get(self, label, id):
        return makeResponse("todo", 200)