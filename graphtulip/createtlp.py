from connector import neo4j, mongo
from neo4j.v1 import ResultError
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
        self.property_id = self.tulip_graph.getStringProperty("neo4j_id")
        self.property_label = self.tulip_graph.getStringProperty("name")
        self.property_labels = self.tulip_graph.getStringProperty("labels")
        self.property_color = self.tulip_graph.getColorProperty("viewColor")
        self.property_size = self.tulip_graph.getSizeProperty("viewSize")
        self.models = []
        mongo_models = mongo.db['models'].find()
        for m in mongo_models:
            self.models.append(m)

    def create(self, params):
        params = tlp.getDefaultPluginParameters('Planar Graph')
        params['nodes'] = 30
        tlp.setSeedOfRandomSequence(random.getrandbits(10))
        tlp.initRandomSequence()
        self.tulip_graph = tlp.importGraph('Planar Graph', params)
        property_id = self.tulip_graph.getStringProperty("neo4j_id")
        property_label = self.tulip_graph.getStringProperty("name")
        property_labels = self.tulip_graph.getStringProperty("labels")
        property_color = self.tulip_graph.getColorProperty("viewColor")
        property_size = self.tulip_graph.getSizeProperty("viewSize")
        for node in self.tulip_graph.nodes():
            property_id[node] = str(node.id)
            property_label[node] = names.get_full_name()
            property_color[node] = tlp.Color(49,130,189)
            property_size[node] = tlp.Size(4, 4, 4)
        for edge in self.tulip_graph.edges():
            property_id[edge] = str(edge.id)
            property_color[edge] = tlp.Color(158,202,225)
        self.tulip_graph.applyLayoutAlgorithm("FM^3 (OGDF)")
        return self.tulip_graph

    def getLabel(self, id, labels):
        model = next((model for model in self.models if model['label'] in labels and 'labeling' in model.keys()), None)
        if model and model['labeling']:
            # q = "MATCH (n:%s) WHERE ID(n) = %s" % (model['label'], id)
            q = "MATCH (n)--(:Link:Prop)--(p:Property:%s) WHERE ID(n) = %s" % (model['labeling'], id)
            q += " RETURN p.value as label"
            r = neo4j.query_neo4j(q)
            try:
                return r.single()['label']
            except ResultError:
                return "id: %s" % id

    def getColor(self, labels):
        for label in eval(labels):
            for model in self.models:
                if model['label'] == label and 'color' in model.keys():
                    color = model['color'].split(',')
                    return tlp.Color(int(color[0].replace('rgb(', '')), int(color[1]), int(color[2][:-1]))
        return tlp.Color(49, 130, 189)

    def addNode(self, record, key, args):
        n = self.tulip_graph.addNode()
        self.property_id[n] = str(record['id_%s' % key])
        self.property_labels[n] = str(record['labels_%s' % key])
        self.property_size[n] = tlp.Size(4, 4, 4)
        if 'color_%s' % key in args.keys() and args['color_%s' % key]:
            color = args['color_%s' % key].split(',')
            self.property_color[n] = tlp.Color(int(color[0].replace('rgb(', '')), int(color[1]), int(color[2][:-1]))
        else:
            self.property_color[n] = self.getColor(str(record['labels_%s' % key]))
        if 'label_%s' % key in record.keys():
            self.property_label[n] = str(record['label_%s' % key])
        else:
            self.property_label[n] = str(self.getLabel(record['id_%s' % key], record['labels_%s' % key]))
        return n

    def addEdge(self, record, key, args, n1, n2, duplicate=False):
        e = self.tulip_graph.addEdge(n1, n2)
        if duplicate:
            self.property_id[e] = 'd%s_%s' % (duplicate, str(record['id_%s' % key]))
        else:
            self.property_id[e] = str(record['id_%s' % key])
        self.property_labels[e] = str(record['labels_%s' % key])
        if 'color_%s' % key in args.keys() and args['color_%s' % key]:
            color = args['color_%s' % key].split(',')
            self.property_color[e] = tlp.Color(int(color[0].replace('rgb(', '')), int(color[1]), int(color[2][:-1]))
        else:
            self.property_color[e] = self.getColor(str(record['labels_%s' % key]))
        if 'label_%s' % key in record.keys() and record['label_%s' % key]:
            self.property_label[e] = str(record['label_%s' % key])
        else:
            self.property_label[e] = str(self.getLabel(record['id_%s' % key], str(record['labels_%s' % key])))
        return e

    def createGraphQuery(self, args):
        query = ""
        match = ""
        optional = ""
        is_optional = False
        n=0
        edges=[]
        print(args)
        for element in args['query'].split('/'):
            property = element.split('->')
            if property[0] and not property[0] == 'AND' and not property[0] == 'OR' and not property[0] == 'NOT':
                print(property[0])
                if 'Link' in property[0]:
                    print("link")
                    query += ' MATCH (n%s)-->(e%s:%s)-->(n%s)' % (n - 1, len(edges), property[0], n)
                    if len(property) > 1:
                        for p in property[1:]:
                            prop = p.split("=")
                            if not (prop[0] == 'AND' or prop[0] == 'OR'):
                                query += " MATCH (e%s:%s)" % (len(edges), property[0])
                                query += "-->(:Prop)-->(:Property:%s {value: '%s'})" % (prop[0], prop[1])
                    edges.append({'source': n - 1, 'target': n})
                else:
                    if len(property) > 1:
                        for p in property[1:]:
                            prop = p.split("=")
                            if not (prop[0] == 'AND' or prop[0] == 'OR'):
                                query += " MATCH (n%s:%s)" % (n, property[0])
                                query += "-->(:Prop)-->(:Property:%s {value: '%s'})" % (prop[0], prop[1])
                    else:
                        query += " MATCH (n%s:%s)" % (n, property[0])
                    n += 1
                if is_optional:
                    optional += ' OPTIONAL' + query
                    is_optional = False
                else:
                    match += query
                query = ''
            elif property[0] == 'OR':
                is_optional = True

        query += match + optional + ' RETURN '
        for i in range(0, n):
            query += "ID(n%s) as id_n%s, labels(n%s) as labels_n%s, " % (i, i, i, i)
        for i, e in enumerate(edges):
            query += "ID(e%s) as id_e%s, labels(e%s) as labels_e%s, " % (i, i, i, i)
        query = query[:-2]
        print(query)
        result = neo4j.query_neo4j(query)

        nodes_done = {}
        edges_done = {}

        for record in result:
            # Nodes
            for i in range(0, n):
                if record['id_n%s' % i] and record['id_n%s' % i] not in nodes_done:
                    nodes_done[record['id_n%s' % i]] = self.addNode(record, 'n%s' % i, args)

            #  Edges
            for i, e in enumerate(edges):
                source = nodes_done[record['id_n%s' % e['source']]]
                target = nodes_done[record['id_n%s' % e['target']]]
                if record['id_e%s' % i] and record['id_e%s' % i] not in edges_done:
                    self.addEdge(record, 'e%s' % i, args, source, target)
                    edges_done[record['id_e%s' % i]] = {'count': 1, 'sources': [source.id], 'targets': [target.id]}
                elif record['id_e%s' % i] and not (source.id in edges_done[record['id_e%s' % i]]['sources'] and target.id in edges_done[record['id_e%s' % i]]['targets']):
                    self.addEdge(record, 'e%s' % i, args, source, target, edges_done[record['id_e%s' % i]]['count'])
                    edges_done[record['id_e%s' % i]]['count'] += 1
                    edges_done[record['id_e%s' % i]]['sources'].append(source.id)
                    edges_done[record['id_e%s' % i]]['targets'].append(target.id)
        return self.tulip_graph

    def createLabelEdgeLabel(self, params):
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

        for record in result:
            if record['id_left'] not in nodes_done:
                left = nodes_done[record['id_left']] = self.addNode(record, 'left', args)
            else:
                left = nodes_done[record['id_left']]
            if record['id_right'] not in nodes_done:
                right = nodes_done[record['id_right']] = self.addNode(record, 'right', args)
            else:
                right = nodes_done[record['id_right']]
            if record['id_edge'] not in edges_done:
                edge = self.addEdge(record, 'edge', args, left, right)
                edges_done.append(record['id_edge'])
            else:
                edge = self.addEdge(record, 'edge', args, left, right, 1)
        return self.tulip_graph

    def createNeighboursById(self, params):  # todo add level of depth
        id, e, label, args = params
        nodes_done = {}
        edges_done = {}

        def execute_query(query, target_to_neigh):
            result = neo4j.query_neo4j(query)
            for record in result:
                if record['id_neigh'] and record['id_target'] not in nodes_done:
                    t = nodes_done[record['id_target']] = self.addNode(record, 'target', args)
                else:
                    t = nodes_done[record['id_target']]
                if record['id_neigh'] and record['id_neigh'] not in nodes_done:
                    n = nodes_done[record['id_neigh']] = self.addNode(record, 'neigh', args)
                else:
                    n = nodes_done[record['id_neigh']]
                if record['id_edge'] and record['id_edge'] not in edges_done:
                    if target_to_neigh:
                        self.addEdge(record, 'edge', args, t, n)
                        edges_done[record['id_edge']] = {'source': [t.id], 'target': [n.id], 'count': 1}
                    else:
                        self.addEdge(record, 'edge', args, n, t)
                        edges_done[record['id_edge']] = {'source': [n.id], 'target': [t.id], 'count': 1}
                else:
                    if target_to_neigh and not (t.id in edges_done[record['id_edge']]['source'] and n.id in edges_done[record['id_edge']]['target']):
                        edges_done[record['id_edge']]['source'].append(t.id)
                        edges_done[record['id_edge']]['target'].append(n.id)
                        edges_done[record['id_edge']]['count'] += 1
                        self.addEdge(record, 'edge', args, t, n, edges_done[record['id_edge']]['count'])
                    elif not (n.id in edges_done[record['id_edge']]['source'] and t.id in edges_done[record['id_edge']]['target']):
                        edges_done[record['id_edge']]['source'].append(n.id)
                        edges_done[record['id_edge']]['target'].append(t.id)
                        edges_done[record['id_edge']]['count'] += 1
                        self.addEdge(record, 'edge', args, n, t, edges_done[record['id_edge']]['count'])


        query = "MATCH (n) WHERE ID(n) = %s WITH n MATCH (n)-[]->(e:%s)-[]->(neigh:%s)" % (id, e, label)
        query += " RETURN ID(n) as id_target"
        query += ", ID(e) as id_edge"
        query += ", ID(neigh) as id_neigh"
        query += ", labels(n) as labels_target"
        query += ", labels(e) as labels_edge"
        query += ", labels(neigh) as labels_neigh"
        if args['label_key_right']:
            query += ", neigh.%s as label_neigh" % args['label_key_right']
        if args['label_key_left']:
            query += ", n.%s as label_target" % args['label_key_left']


        execute_query(query, False)

        query = "MATCH (n) WHERE ID(n) = %s WITH n MATCH (n)<-[]-(e:%s)<-[]-(neigh:%s)" % (id, e, label)
        query += " RETURN ID(n) as id_target"
        query += ", ID(e) as id_edge"
        query += ", ID(neigh) as id_neigh"
        query += ", labels(n) as labels_target"
        query += ", labels(e) as labels_edge"
        query += ", labels(neigh) as labels_neigh"
        if args['label_key_right']:
            query += ", neigh.%s as label_neigh" % args['label_key_right']
        if args['label_key_left']:
            query += ", n.%s as label_target" % args['label_key_left']

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
            query += ", ID(e) as id_edge"
            query += ", ID(neigh) as id_neigh"
            query += ", labels(n) as labels_target"
            query += ", labels(e) as labels_edge"
            query += ", labels(neigh) as labels_neigh"
            if args['label_key_right']:
                query += ", neigh.%s as label_neigh" % args['label_key_right']
            if args['label_key_left']:
                query += ", n.%s as label_target" % args['label_key_left']

            execute_query(query, False)

        return self.tulip_graph
