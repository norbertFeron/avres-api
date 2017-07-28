from connector import neo4j
from tulip import *
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


class CreateTlp(object):
    def __init__(self):
        super(CreateTlp, self).__init__()
        self.tulip_graph = tlp.newGraph()
        self.tulip_graph.setName('graph-ryder-generated')

    def create(self, params):
        # todo read and create the graph
        params = tlp.getDefaultPluginParameters('Random General Graph')
        self.tulip_graph = tlp.importGraph('Random General Graph', params)
        return self.tulip_graph

    def createLabelEdgeLabel(self, params):
        property_id = self.tulip_graph.getIntegerProperty("neo4j_id")
        property_label = self.tulip_graph.getStringProperty("name")
        property_color = self.tulip_graph.getColorProperty("viewColor")
        l1, e, l2, args = params
        query = "MATCH (n1:%s)-[]->(e:%s)-[]->(n2:%s) RETURN ID(n1) as id_1" % (l1, e, l2)
        if args['label_key_left']:
            query += ", n1.%s as label_left" % args['label_key_left']
        query += ", ID(e) as id_e, labels(e) as labels_e, "
        query += "ID(n2) as id_2"
        if args['label_key_right']:
            query += ", n2.%s as label_right" % args['label_key_right']
        result = neo4j.query_neo4j(query)
        nodes_done = {}
        edges_done = []
        for record in result:
            if record['id_1'] not in nodes_done:
                n1 = self.tulip_graph.addNode()
                property_id[n1] = record['id_1']
                property_color[n1] = tlp.Color(44, 162, 95)
                if 'label_left' in record.keys() and record['label_left']:
                    property_label[n1] = record['label_left']
                nodes_done[record['id_1']] = n1
            else:
                n1 = nodes_done[record['id_1']]
            if record['id_2'] not in nodes_done:
                n2 = self.tulip_graph.addNode()
                property_id[n2] = record['id_2']
                property_color[n2] = tlp.Color(44, 162, 95)
                if 'label_right' in record.keys() and record['label_right']:
                    property_label[n2] = record['label_right']
                nodes_done[record['id_2']] = n2
            else:
                n2 = nodes_done[record['id_2']]
            if record['id_e'] not in edges_done:
                e = self.tulip_graph.addEdge(n1, n2)
                property_id[e] = record['id_e']
                property_label[e] = str(record['labels_e'])
                property_color[e] = tlp.Color(153, 216, 201)
        return self.tulip_graph

    def createNeighboursById(self, params):  # todo add level of depth
        property_id = self.tulip_graph.getIntegerProperty("neo4j_id")
        property_label = self.tulip_graph.getStringProperty("name")
        property_color = self.tulip_graph.getColorProperty("viewColor")
        id, e, args = params
        query = "MATCH (n) WHERE ID(n) = %s WITH n MATCH (n)-[]-(e:%s)-[]-(neigh)" % (id, e)
        query += " RETURN ID(n) as id_target"
        query += ", ID(e) as id_e, labels(e) as labels_e"
        query += ", ID(neigh) as id_neigh, labels(neigh) as label_neigh"
        result = neo4j.query_neo4j(query)
        nodes_done = {}
        edges_done = []
        for record in result:
            if record['id_target'] not in nodes_done:
                t = self.tulip_graph.addNode()
                property_id[t] = record['id_target']
                property_label[t] = str(record['id_target'])
                nodes_done[record['id_target']] = t
            else:
                t = nodes_done[record['id_target']]
            if record['id_neigh'] not in nodes_done:
                n = self.tulip_graph.addNode()
                property_id[n] = record['id_neigh']
                property_label[n] = str(record['id_neigh'])
                #  todo add labels(neigh) result
                nodes_done[record['id_neigh']] = n
            else:
                n = nodes_done[record['id_neigh']]
            if record['id_e'] not in edges_done:
                e = self.tulip_graph.addEdge(t, n)  # todo manage edge direction
                property_id[e] = record['id_e']
                property_label[e] = str(record['labels_e'])
                property_color[e] = tlp.Color(51, 122, 183)
            #  todo link neighbours together
        return self.tulip_graph
