from connector import neo4j
from flask_restful import Resource, reqparse
from routes.utils import makeResponse

parser = reqparse.RequestParser()
parser.add_argument('keys', action='append')


class GetLabels(Resource):
    """
       @api {get} /getLabels/:label Get possible labels for a generic label 
       @apiName GetLabels
       @apiGroup Generic
       @apiDescription Return the list of possible labels for a generic one.
       @apiParam {String} label Label
       @apiSuccess {Array} result Array of labels
       @apiSuccessExample {json} Success-Response:
       http://api-url/getLabels/Link
       HTTP/1.1 200 OK
       ["Link", "Locate", "Acquaintance", "Financial", "Event", "Action", "Blood", "Sexual", "Support"]
    """
    def get(self, label):
        query = "MATCH (n:%s) WITH n UNWIND labels(n) as l RETURN COLLECT(DISTINCT l) as labels" % label
        result = neo4j.query_neo4j(query)
        return makeResponse(result.single()['labels'], 200)


class GetPropertiesByLabel(Resource):
    """
       @api {get} /GetPropertiesByLabel/:label Get possible property for a label 
       @apiName GetPropertiesByLabel
       @apiGroup Generic
       @apiDescription Get possible property for a label  
       @apiParam {String} label Label
       @apiSuccess {Array} result Array of property.
    """
    def get(self, label):
        query = "MATCH (n:%s) WITH n UNWIND keys(n) as k RETURN COLLECT(DISTINCT k) as keys" % label
        result = neo4j.query_neo4j(query)
        return makeResponse(result.single()['keys'], 200)


class GetPropertyValueByLabel(Resource):
    """
       @api {get} /GetPropertyValueByLabel/:label/:property Get possible value by property/label 
       @apiName GetPropertyValueByLabel
       @apiGroup Generic
       @apiDescription Get possible property value for a label  
       @apiParam {String} label Label
       @apiParam {String} property Property
       @apiSuccess {Array} result Array of value.
    """
    def get(self, label, key):
        query = "MATCH (n:%s) RETURN COLLECT(DISTINCT n.%s) as values" % (label, key)
        result = neo4j.query_neo4j(query)
        return makeResponse(result.single()['values'], 200)


class GetByLabel(Resource):
    def get(self, label):
        """
           @api {get} /GetByLabel/:label Get elements by label 
           @apiName GetByLabel
           @apiGroup Generic
           @apiDescription Get elements for a label  
           @apiParam {String} label Label
           @apiParam {Args} keys Keys wanted for each element
           @apiSuccess {Array} result Array of element.
        """
        args = parser.parse_args()
        keys = args['keys']
        query = "MATCH (n:%s) RETURN ID(n) as id" % label
        if keys:
            for key in keys:
                query += ", n.%s as %s" % (key, key)
        result = neo4j.query_neo4j(query)
        response = []
        for record in result:
            person = {'id': record['id']}
            if keys:
                for key in keys:
                    person[key] = record[key]
            response.append(person)
        return makeResponse(response, 200)


class GetById(Resource):
    def get(self, label, id):
        return makeResponse("todo", 200)


class GetByLabelAndId(Resource):
    def get(self, label, id):
        return makeResponse("todo", 200)