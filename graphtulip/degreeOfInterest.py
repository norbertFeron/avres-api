import configparser
from tulip import *

config = configparser.ConfigParser()
config.read("config.ini")


class DOIContext(object):
    """docstring for DOIContexte"""

    def __init__(self, graph):
        super(DOIContext, self).__init__()
        self.graph = graph
        self.original_graph = self.graph

        self.API_metric = self.original_graph.getDoubleProperty('API')
        self.API_metric.setAllNodeValue(1.0)
        self.UI_metric = self.original_graph.getDoubleProperty('UI')
        self.UI_metric.setAllNodeValue(1.0)
        self.DOI_metric = self.original_graph.getDoubleProperty('DOI')

    # todo: search with neo4j the focus
    def get_focus_node(self):
        selection = self.original_graph.getBooleanProperty('viewSelection')
        focus = None
        for n in self.original_graph.getNodes():
            if selection[n]:
                focus = n
                break
        return focus

    def get_node(self, type, node_id):
        node = None
        propertie = self.original_graph.getProperty(type)
        for n in self.original_graph.getNodes():
            if propertie[n] == node_id:
                node = n
                break
        print(node)
        return node

    def set_API(self, double_property):
        for n in self.original_graph.getNodes():
            self.API_metric[n] = double_property[n]

    def compute_DOI(self, focus_node):
        dist = self.original_graph.getIntegerProperty('distance_to_focus')
        print(focus_node)
        tlp.maxDistance(self.original_graph, focus_node, dist, tlp.UNDIRECTED)
        for n in self.original_graph.getNodes():
            self.DOI_metric[n] = self.API_metric[n] + self.UI_metric[n] - dist[n]

    def compute_context_subgraph(self, focus_node, max_size=20):
        color = self.original_graph.getColorProperty('viewColor')
        color.setAllNodeValue(tlp.Color(255, 64, 64))
        #focus_node = self.get_focus_node()
        self.compute_DOI(focus_node)
        focus_nodeset = set()
        candidates = [focus_node]
        while len(candidates) > 0 and len(focus_nodeset) < 20:
            c = sorted(candidates, key=lambda x: self.DOI_metric[x]).pop()
            candidates.pop(candidates.index(c))
            focus_nodeset.add(c)
            color[c] = tlp.Color(0, 0, 255)
            for n in self.original_graph.getInOutNodes(c):
                if not n in focus_nodeset and not n in candidates:
                    candidates.append(n)
        context_subgraph = self.original_graph.inducedSubGraph(focus_nodeset)
        context_subgraph.setName('context')
        return context_subgraph

def create(graph_id, type, node_id):
    graph = tlp.loadGraph("%s%s.tlp" % (config['exporter']['tlp_path'], "complete"))
    doi = DOIContext(graph)

    dataset = tlp.getDefaultPluginParameters('Degree', graph)
    degree = doi.original_graph.getDoubleProperty('degree')
    graph.applyDoubleAlgorithm('Degree', degree, dataset)

    dataset = tlp.getDefaultPluginParameters('Betweenness Centrality', graph)
    bc = doi.original_graph.getDoubleProperty('betweenness')
    graph.applyDoubleAlgorithm('Betweenness Centrality', bc, dataset)

    doi.set_API(bc)

    # f = doi.get_focus_node()
    f = doi.get_node(type, node_id)
    doi.compute_DOI(f)
    context_subgraph = doi.compute_context_subgraph(f)
    tlp.saveGraph(context_subgraph, "%s%s.tlp" % (config['exporter']['tlp_path'], graph_id))
