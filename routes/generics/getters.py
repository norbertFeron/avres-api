from neo4j.v1 import ResultError

from connector import neo4j
from flask_restful import Resource, reqparse
from routes.utils import makeResponse, addargs

parser = reqparse.RequestParser()
parser.add_argument('keys', action='append')
parser.add_argument('filters', action='append')
parser.add_argument('attrs', action='append')
parser.add_argument('hydrate')


class GetLabels(Resource):
    """
      @api {get} /getLabels/ Get all labels
      @apiName GetLabels
      @apiGroup Getters
      @apiDescription Return the list of possible labels.
      @apiParam {String} label Label
      @apiSuccess {Array} result Array of labels
   """
    def get(self):
        query = "MATCH (n) WITH n UNWIND labels(n) as l RETURN COLLECT(DISTINCT l) as labels"
        result = neo4j.query_neo4j(query)
        return makeResponse(result.single()['labels'], 200)


class GetLabelsByLabel(Resource):
    """
      @api {get} /getLabels/:label Get labels by label 
      @apiName GetLabelsByLabel
      @apiGroup Getters
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


class GetLabelsById(Resource):
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
    def get(self, id):
        query = "MATCH (n) WHERE ID(n) = %s WITH n UNWIND labels(n) as l RETURN COLLECT(DISTINCT l) as labels" % id
        result = neo4j.query_neo4j(query)
        return makeResponse(result.single()['labels'], 200)


class GetPropertiesByLabel(Resource):
    """
       @api {get} /GetPropertiesbel Get properties by label 
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
       @api {get} /GetAttributes/:label Get properties by label 
       @apiName GetAttributesByLabel
       @apiGroup Getters
       @apiDescription Get possible attributes for a label  
       @apiParam {String} label Label
       @apiSuccess {Array} result Array of attributes.
    """
    def get(self, label):
        query = "MATCH (n:%s)-[:HAS]->(:Property)-[:IS]->(k) RETURN COLLECT(DISTINCT labels(k)) as attr" % label
        result = neo4j.query_neo4j(query)
        return makeResponse(result.single()['attr'], 200)


class GetPropertyValue(Resource):
    """
       @api {get} /GetPropertyValue/:label/:property Get value by property/label 
       @apiName GetPropertyValueByLabel
       @apiGroup Getters
       @apiDescription Get possible property value for a label  
       @apiParam {String} label Label
       @apiParam {String} property Property
       @apiSuccess {Array} result Array of value.
    """
    def get(self, key):
        query = "MATCH (n) RETURN COLLECT(DISTINCT n.%s) as values" % key
        result = neo4j.query_neo4j(query)
        return makeResponse(result.single()['values'], 200)


class GetPropertyValueByLabel(Resource):
    """
       @api {get} /GetPropertyValue/:label/:property Get value by property/label 
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


class GetByLabel(Resource):  # todo convert date node to readable date when hydrate
    """
       @api {get} /get/:label Get elements by label 
       @apiName GetByLabel
       @apiGroup Getters
       @apiDescription Get elements for a label 
       @apiParam {String} label Label
       @apiParam {keys} keys Keys wanted for each property of the element (* for all)
       @apiParam {attrs} attr attributes wanted for each element (* for all)
       @apiParam {hydrate} hydrate != 0 to hydrate attrs with info
       @apiParam {Filters} filter Filters on property
       @apiSuccess {Array} result Array of element.
    """
    def get(self, label):
        args = parser.parse_args()
        keys = args['keys']
        filters = args['filters']
        query = "MATCH (n:%s)" % label
        if filters:
            query += "WHERE"
            for filter in filters:
                query += " n.%s = '%s' AND" % (filter.split(':')[0], filter.split(':')[1])
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
        response = {}
        for record in result:
            if not record['id'] in response.keys():
                response[record['id']] = {}
            if keys:
                for key in keys:
                    response[record['id']][key] = record[key]
        attrs = args['attrs']
        if attrs and '*' in attrs:
            attrs = []
            q = "MATCH (n:%s)-[:HAS]->(:Property)-[:IS]->(k)" % label
            q += " RETURN COLLECT(DISTINCT labels(k)) as attr"
            result = neo4j.query_neo4j(q)
            attributes = result.single()['attr']
            for a in attributes:
                if 'Attribute' in a:
                    a.remove('Attribute')
                attrs.append(a[0])  # Unpack
        if attrs:
            for attribute in attrs:
                query = "MATCH (n:%s)" % label
                query += " WITH n"
                query += " MATCH (n)-[:HAS]->(:Property)-[:IS]->(%s:%s)" % (attribute, attribute)
                query += " RETURN ID(n) as id, collect(DISTINCT ID(%s)) as %s " % (attribute, attribute)
                result = neo4j.query_neo4j(query)
                for record in result:
                    if not record['id'] in response.keys():
                        response[record['id']] = {}
                    if not args['hydrate'] or args['hydrate'] == str(0):
                        response[record['id']][attribute] = record[attribute]
                    else:
                        response[record['id']][attribute] = []
                        for a in record[attribute]:
                            q = "MATCH (n) WHERE ID(n) = %s WITH n UNWIND keys(n) as k" % a
                            q += " RETURN COLLECT(DISTINCT k) as keys"
                            result = neo4j.query_neo4j(q)
                            keys = result.single()['keys']
                            query = "MATCH (n) WHERE ID(n) = %s RETURN ID(n) as id" % a
                            for key in keys:
                                query += ", n.%s as %s" % (key, key)
                            result = neo4j.query_neo4j(query)
                            try:
                                res = result.single()
                            except ResultError:
                                return makeResponse("Impossible to find this id", 400)
                            attr = {'id': res['id']}
                            if keys:
                                for key in keys:
                                    attr[key] = res[key]
                            response[record['id']][attribute].append(attr)
        return makeResponse(response, 200)


class GetById(Resource):
    """
       @api {get} /get/:id Get an element by id 
       @apiName GetById
       @apiGroup Getters
       @apiDescription Get element by neo4j id
       @apiParam {Integer} id id
       @apiParam {keys} keys Keys wanted for each property of the element (* for all)
       @apiParam {attrs} attr attributes wanted for each element (* for all)
       @apiParam {hydrate} hydrate != 0 to hydrate attrs with info
       @apiSuccess {Element} the element
    """
    def get(self, id):  # Multiple request
        args = parser.parse_args()
        keys = args['keys']
        query = "MATCH (n) WHERE ID(n) = %s RETURN ID(n) as id" % id
        if keys and '*' in keys:
            q = "MATCH (n) WHERE ID(n) = %s WITH n UNWIND keys(n) as k RETURN COLLECT(DISTINCT k) as keys" % id
            result = neo4j.query_neo4j(q)
            keys = result.single()['keys']
        if keys:
            for key in keys:
                query += ", n.%s as %s" % (key, key)
        query += addargs()
        result = neo4j.query_neo4j(query)
        try:
            res = result.single()
        except ResultError:
            return makeResponse("Impossible to find this id", 400)
        element = {'id': res['id']}
        if keys:
            for key in keys:
                element[key] = res[key]
        args = parser.parse_args()
        attrs = args['attrs']
        if attrs and '*' in attrs:
            attrs = []
            q = "MATCH (n)-[:HAS]->(:Property)-[:IS]->(k)"
            q += " WHERE ID(n) = %s RETURN COLLECT(DISTINCT labels(k)) as attr" % id
            result = neo4j.query_neo4j(q)
            attributes = result.single()['attr']
            for a in attributes:
                if 'Attribute' in a:
                    a.remove('Attribute')
                attrs.append(a[0])  # Unpack
        if attrs:
            for attribute in attrs:
                query = "MATCH (n) WHERE ID(n) = %s" % id
                query += " WITH n"
                query += " MATCH (n)-[:HAS]->(:Property)-[:IS]->(%s:%s)" % (attribute, attribute)
                query += " RETURN collect(DISTINCT ID(%s)) as %s " % (attribute, attribute)
                result = neo4j.query_neo4j(query)
                try:
                    res = result.single()
                except ResultError:
                    return makeResponse("Impossible to find this id", 400)
                if not args['hydrate'] or args['hydrate'] == 0:
                    element[attribute] = res[attribute]
                else:
                    element[attribute] = []
                    for a in res[attribute]:
                        q = "MATCH (n) WHERE ID(n) = %s WITH n UNWIND keys(n) as k RETURN COLLECT(DISTINCT k) as keys" % a
                        result = neo4j.query_neo4j(q)
                        keys = result.single()['keys']
                        query = "MATCH (n) WHERE ID(n) = %s RETURN ID(n) as id" % a
                        for key in keys:
                            query += ", n.%s as %s" % (key, key)
                        result = neo4j.query_neo4j(query)
                        try:
                            res = result.single()
                        except ResultError:
                            return makeResponse("Impossible to find this id", 400)
                        attr = {'id': res['id']}
                        if keys:
                            for key in keys:
                                attr[key] = res[key]
                        element[attribute].append(attr)
        return makeResponse(element, 200)
