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

    def createlabeledgelabel(self, params):
        property_id = self.tulip_graph.getIntegerProperty("neo4j_id")
        property_label = self.tulip_graph.getStringProperty("name")
        l1, e, l2 = params
        query = "MATCH (n1:%s)-[]-(e:%s)-[]-(n2:%s) RETURN ID(n1) as id_1, ID(e) as id_e, labels(e) as labels_e, " \
                "ID(n2) as id_2" % (l1, e, l2)
        result = neo4j.query_neo4j(query)
        nodes_done = {}
        edges_done = []
        for record in result:
            if record['id_1'] not in nodes_done:
                n1 = self.tulip_graph.addNode()
                property_id[n1] = record['id_1']
                property_label[n1] = "myNode_1"
                nodes_done[record['id_1']] = n1
            else:
                n1 = nodes_done[record['id_1']]
            if record['id_2'] not in nodes_done:
                n2 = self.tulip_graph.addNode()
                property_id[n2] = record['id_2']
                property_label[n2] = "myNode_2"
                nodes_done[record['id_2']] = n2
            else:
                n2 = nodes_done[record['id_2']]
            if record['id_e'] not in edges_done:
                e = self.tulip_graph.addEdge(n1, n2)
                property_id[e] = record['id_e']
                property_label[e] = str(record['labels_e'])
        return self.tulip_graph
