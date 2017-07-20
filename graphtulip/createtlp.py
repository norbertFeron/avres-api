from tulip import *
from py2neo import *
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


class CreateTlp(object):
    def __init__(self):
        super(CreateTlp, self).__init__()
        print('Initializing')

        self.neo4j_graph = Graph(host=config['neo4j']['url'], user=config['neo4j']['user'], password=config['neo4j']['password'])
        self.tulip_graph = tlp.newGraph()
        self.tulip_graph.setName('xxx')

    def create(self, params, private_gid):
        # todo read and create the graph
        params = tlp.getDefaultPluginParameters('Random General Graph')
        self.tulip_graph = tlp.importGraph('Random General Graph', params)
        tlp.saveGraph(self.tulip_graph, "%s%s.tlp" % (config['exporter']['tlp_path'], private_gid))
