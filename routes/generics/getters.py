from connector import neo4j
from flask_restful import Resource, reqparse
from routes.utils import makeResponse, addargs

parser = reqparse.RequestParser()
parser.add_argument('keys', action='append')
parser.add_argument('filters', action='append')


class GetLabelsByLabel(Resource):
    def get(self, label):
        """
          @api {get} /getLabels/:label Get labels by label 
          @apiName GetLabels
          @apiGroup Getters
          @apiDescription Return the list of possible labels for a generic one.
          @apiParam {String} label Label
          @apiSuccess {Array} result Array of labels
          @apiSuccessExample {json} Success-Response:
          http://api-url/getLabels/Link
          HTTP/1.1 200 OK
          ["Link", "Locate", "Acquaintance", "Financial", "Event", "Action", "Blood", "Sexual", "Support"]
       """
        query = "MATCH (n:%s) WITH n UNWIND labels(n) as l RETURN COLLECT(DISTINCT l) as labels" % label
        result = neo4j.query_neo4j(query)
        return makeResponse(result.single()['labels'], 200)


class GetLabelsById(Resource):
    def get(self, id):
        """
           @api {get} /getLabels/:id Get labels by id 
           @apiName GetLabels
           @apiGroup Getters
           @apiDescription Return the list of possible labels for a neo4j id.
           @apiParam {Integer} id Id
           @apiSuccess {Array} result Array of labels
           @apiSuccessExample {json} Success-Response:
           http://api-url/getLabels/123456
           HTTP/1.1 200 OK
           ["Link", "Locate"]
        """
        query = "MATCH (n) WHERE ID(n) = %s WITH n UNWIND labels(n) as l RETURN COLLECT(DISTINCT l) as labels" % id
        result = neo4j.query_neo4j(query)
        return makeResponse(result.single()['labels'], 200)


class GetPropertiesByLabel(Resource):
    """
       @api {get} /GetPropertiesByLabel/:label Get properties by label 
       @apiName GetPropertiesByLabel
       @apiGroup Getters
       @apiDescription Get possible property for a label  
       @apiParam {String} label Label
       @apiSuccess {Array} result Array of property.
    """
    def get(self, label):
        query = "MATCH (n:%s) WITH n UNWIND keys(n) as k RETURN COLLECT(DISTINCT k) as keys" % label
        result = neo4j.query_neo4j(query)
        return makeResponse(result.single()['keys'], 200)


class GetAttributesByLabel(Resource):
    """
       @api {get} /GetAttributesByLabel/:label Get properties by label 
       @apiName GetAttributesByLabel
       @apiGroup Getters
       @apiDescription Get possible attributes for a label  
       @apiParam {String} label Label
       @apiSuccess {Array} result Array of attributes.
    """
    def get(self, label):
        query = "MATCH (n:%s)-[:HAVE]->(a:Attribute) WITH n,a UNWIND a.type as attr RETURN COLLECT(" \
                "DISTINCT attr) as attributes" % label
        result = neo4j.query_neo4j(query)
        return makeResponse(result.single()['attributes'], 200)


class GetPropertyValueByLabel(Resource):
    """
       @api {get} /GetPropertyValueByLabel/:label/:property Get value by property/label 
       @apiName GetPropertyValueByLabel
       @apiGroup Getters
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
           @apiGroup Getters
           @apiDescription Get elements for a label, pass keys are arguments (* for all args)  
           @apiParam {String} label Label
           @apiParam {Keys} keys Keys wanted for each element
           @apiParam {Filters} filter Filters on property
           @apiSuccess {Array} result Array of element.
        """
        args = parser.parse_args()
        keys = args['keys']
        filters = args['filters']
        query = "MATCH (n:%s)" % label
        if filters:
            query += "WHERE"
            for filter in filters:
                query += " n.%s = %s AND" % (filter.split(':')[0], filter.split(':')[1])
            query = query[:-4]
        query += " RETURN ID(n) as id"
        if keys:
            if '*' in keys:
                q = "MATCH (n:%s) WITH n UNWIND keys(n) as k RETURN COLLECT(DISTINCT k) as keys" % label
                result = neo4j.query_neo4j(q)
                keys = result.single()['keys']
            for key in keys:
                query += ", n.%s as %s" % (key, key)
        query += addargs()
        result = neo4j.query_neo4j(query)
        response = []
        for record in result:
            element = {'id': record['id']}
            if keys:
                for key in keys:
                    element[key] = record[key]
            response.append(element)
        return makeResponse(response, 200)


class GetById(Resource):
    def get(self, id):
        """
           @api {get} /GetById/:id Get element by id 
           @apiName GetById
           @apiGroup Getters
           @apiDescription Get element by neo4j id, pass keys are arguments (* for all args)  
           @apiParam {String} label Label
           @apiParam {Args} keys Keys wanted for each element
           @apiSuccess {Element} the element
        """
        args = parser.parse_args()
        keys = args['keys']
        query = "MATCH (n) WHERE ID(n) = %s RETURN ID(n) as id" % (id)
        if '*' in keys:
            q = "MATCH (n) WHERE ID(n) = %s WITH n UNWIND labels(n) as l RETURN COLLECT(DISTINCT l) as labels" % id
            result = neo4j.query_neo4j(q)
            labels = result.single()['labels']
            label = ''
            for l in labels:
                label += l + ":"
            label = label[:-1]
        if keys:
            if '*' in keys:
                q = "MATCH (n:%s) WITH n UNWIND keys(n) as k RETURN COLLECT(DISTINCT k) as keys" % label
                result = neo4j.query_neo4j(q)
                keys = result.single()['keys']
            for key in keys:
                query += ", n.%s as %s" % (key, key)
        query += addargs()
        result = neo4j.query_neo4j(query)
        res = result.single()
        element = {'id': res['id']}
        if keys:
            for key in keys:
                element[key] = res[key]
        return makeResponse(element, 200)
