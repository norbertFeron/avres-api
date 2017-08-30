from connector import neo4j, mongo
from tulip import *
import configparser
import names
import random

config = configparser.ConfigParser()
config.read("config.ini")


class CreateTlp(object):
    def __init__(self):
        super(CreateTlp, self).__init__()
        self.tulip_graph = tlp.newGraph()
        self.tulip_graph.setName('graph-ryder-generated')

    def create(self, params):
        params = tlp.getDefaultPluginParameters('Planar Graph')
        params['nodes'] = 30
        tlp.setSeedOfRandomSequence(random.getrandbits(10))
        tlp.initRandomSequence()
        self.tulip_graph = tlp.importGraph('Planar Graph', params)
        property_label = self.tulip_graph.getStringProperty("name")
        property_color = self.tulip_graph.getColorProperty("viewColor")
        for node in self.tulip_graph.nodes():
            property_label[node] = names.get_full_name()
            property_color[node] = tlp.Color(49,130,189)
        for edge in self.tulip_graph.edges():
            property_color[edge] = tlp.Color(158,202,225)
        return self.tulip_graph

    def createLabelEdgeLabel(self, params):
        models = []
        mongo_models = mongo.db['models'].find()
        for m in mongo_models:
            models.append(m)
        property_id = self.tulip_graph.getIntegerProperty("neo4j_id")
        property_label = self.tulip_graph.getStringProperty("name")
        property_color = self.tulip_graph.getColorProperty("viewColor")
        l1, e, l2, args = params
        query = "MATCH (left:%s)-[]->(edge:%s)-[]->(right:%s) RETURN" % (l1, e, l2)
        query += " ID(left) as id_left"
        query += ", ID(edge) as id_edge"
        query += ", ID(right) as id_right"
        query += ", labels(left) as labels_left "
        query += ", labels(edge) as labels_edge "
        query += ", labels(right) as labels_right "
        if args['label_key_left']:
            query += ", left.%s as label_left" % args['label_key_left']
        if args['label_key_edge']:
            query += ", edge.%s as label_edge " % args['label_key_edge']
        if args['label_key_right']:
            query += ", right.%s as label_right" % args['label_key_right']
        result = neo4j.query_neo4j(query)
        nodes_done = {}
        edges_done = []

        def getLabel(id, labels):
            model = next((model for model in models if model['label'] in labels and 'labeling' in model.keys()), None)
            if model:
                q = "MATCH (n:%s) WHERE ID(n) = %s RETURN n.%s as label" % (model['label'], id, model['labeling'])
                r = neo4j.query_neo4j(q)
                return r.single()['label']
            else:
                return 'No labeling options'

        def getColor(labels):
            for label in eval(labels):
                for model in models:
                    if model['label'] == label and 'color' in model.keys():
                        color = model['color'].split(',')
                        return tlp.Color(int(color[0].replace('rgb(', '')), int(color[1]), int(color[2][:-1]))
            return tlp.Color(49, 130, 189)

        def addNode(graph, record, key, args):
            n = graph.addNode()
            property_id[n] = record['id_%s' % key]
            if args['color_%s' % key]:
                color = args['color_%s' % key].split(',')
                property_color[n] = tlp.Color(int(color[0].replace('rgb(', '')), int(color[1]), int(color[2][:-1]))
            else:
                property_color[n] = getColor(str(record['labels_%s' % key]))
            if 'label_%s' % key in record.keys():
                property_label[n] = str(record['label_%s' % key])
            else:
                property_label[n] = str(getLabel(record['id_%s' % key], str(record['labels_%s' % key])))
            return n

        def addEdge(graph, record, key, args, n1, n2):
            e = graph.addEdge(n1, n2)
            property_id[e] = record['id_%s' % key]
            if args['color_%s' % key]:
                color = args['color_%s' % key].split(',')
                property_color[e] = tlp.Color(int(color[0].replace('rgb(', '')), int(color[1]), int(color[2][:-1]))
            else:
                property_color[e] = getColor(str(record['labels_%s' % key]))
            if 'label_%s' % key in record.keys() and record['label_%s' % key]:
                property_label[e] = str(record['label_%s' % key])
            else:
                property_label[e] = str(getLabel(record['id_%s' % key], str(record['labels_%s' % key])))
            return e

        for record in result:
            if record['id_left'] not in nodes_done:
                left = nodes_done[record['id_left']] = addNode(self.tulip_graph, record, 'left', args)
            else:
                left = nodes_done[record['id_left']]
            if record['id_right'] not in nodes_done:
                right = nodes_done[record['id_right']] = addNode(self.tulip_graph, record, 'right', args)
            else:
                right = nodes_done[record['id_right']]
            if record['id_edge'] not in edges_done:
                edge = addEdge(self.tulip_graph, record, 'edge', args, left, right)
        return self.tulip_graph

    def createNeighboursById(self, params):  # todo add level of depth
        property_id = self.tulip_graph.getIntegerProperty("neo4j_id")
        property_label = self.tulip_graph.getStringProperty("name")
        property_color = self.tulip_graph.getColorProperty("viewColor")
        id, e, label, args = params
        nodes_done = {}
        edges_done = []

        def execute_query(query, target_to_neigh):
            result = neo4j.query_neo4j(query)
            for record in result:
                if record['id_target'] not in nodes_done:
                    t = self.tulip_graph.addNode()
                    property_id[t] = record['id_target']
                    if 'label_target' in record.keys() and type(record['label_target']) is str:
                        property_label[t] = record['label_target']
                    else:
                        property_label[t] = str(record['id_target'])
                    if args['color_left']:
                        color = args['color_left'].split(',')
                        property_color[t] = tlp.Color(int(color[0].replace('rgb(', '')), int(color[1]), int(color[2][:-1]))
                    else:
                        property_color[t] = tlp.Color(49, 130, 189)
                    nodes_done[record['id_target']] = t
                else:
                    t = nodes_done[record['id_target']]
                if record['id_neigh'] not in nodes_done:
                    n = self.tulip_graph.addNode()
                    property_id[n] = record['id_neigh']
                    if 'label_neigh' in record.keys() and type(record['label_neigh']) is str:
                        property_label[n] = record['label_neigh']
                    else:
                        property_label[n] = str(record['id_neigh'])
                    if args['color_right']:
                        color = args['color_right'].split(',')
                        property_color[n] = tlp.Color(int(color[0].replace('rgb(', '')), int(color[1]), int(color[2][:-1]))
                    else:
                        property_color[n] = tlp.Color(49, 130, 189)
                    #  todo add labels(neigh) result
                    nodes_done[record['id_neigh']] = n
                else:
                    n = nodes_done[record['id_neigh']]
                if record['id_e'] not in edges_done:
                    if target_to_neigh:
                        e = self.tulip_graph.addEdge(t, n)
                    else:
                        e = self.tulip_graph.addEdge(n, t)
                    property_id[e] = record['id_e']
                    property_label[e] = str(record['labels_e'])
                    if args['color_edge']:
                        color = args['color_edge'].split(',')
                        property_color[e] = tlp.Color(int(color[0].replace('rgb(', '')), int(color[1]), int(color[2][:-1]))
                    else:
                        property_color[e] = tlp.Color(158, 202, 225)

        query = "MATCH (n) WHERE ID(n) = %s WITH n MATCH (n)-[]->(e:%s)-[]->(neigh:%s)" % (id, e, label)
        query += " RETURN ID(n) as id_target"
        if args['label_key_left']:
            query += ", n.%s as label_target" % args['label_key_left']
        query += ", ID(e) as id_e, labels(e) as labels_e"
        query += ", ID(neigh) as id_neigh"
        if args['label_key_right']:
            query += ", neigh.%s as label_neigh" % args['label_key_right']


        execute_query(query, False)

        query = "MATCH (n) WHERE ID(n) = %s WITH n MATCH (n)<-[]-(e:%s)<-[]-(neigh:%s)" % (id, e, label)
        query += " RETURN ID(n) as id_target"
        query += ", ID(e) as id_e, labels(e) as labels_e"
        query += ", ID(neigh) as id_neigh, labels(neigh) as label_neigh"

        execute_query(query, True)

        if args['depth']:
            #  todo correct depth only works when n is same label as neigh
            i = 1
            while i < int(args['depth']):
                i += 1
                nodes_id = list(nodes_done.keys())
                for id_neigh in nodes_id:
                    query = "MATCH (n) WHERE ID(n) = %s WITH n MATCH (n)-[]->(e:%s)-[]->(neigh:%s)" % (id_neigh, e, label)
                    query += " RETURN ID(n) as id_target"
                    query += ", ID(e) as id_e, labels(e) as labels_e"
                    query += ", ID(neigh) as id_neigh, labels(neigh) as label_neigh"
                    execute_query(query, False)

                    query = "MATCH (n) WHERE ID(n) = %s WITH n MATCH (n)<-[]-(e:%s)<-[]-(neigh:%s)" % (id_neigh, e, label)
                    query += " RETURN ID(n) as id_target"
                    query += ", ID(e) as id_e, labels(e) as labels_e"
                    query += ", ID(neigh) as id_neigh, labels(neigh) as label_neigh"
                    execute_query(query, True)

        nodes_id = list(nodes_done.keys())
        for id_neigh in nodes_id:
            query = "MATCH (n) WHERE ID(n) = %s WITH n " % id_neigh
            query += "MATCH (n)-[]->(e:%s)-[]->(neigh) WHERE ID(neigh) IN %s" % (e, nodes_id)
            query += " RETURN ID(n) as id_target"
            query += ", ID(e) as id_e, labels(e) as labels_e"
            query += ", ID(neigh) as id_neigh, labels(neigh) as label_neigh"

            execute_query(query, False)

        return self.tulip_graph
