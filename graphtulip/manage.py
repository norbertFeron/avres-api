from tulip import *
from loader.loader import load_doi

from graphtulip.degreeOfInterest import ComputeDoi

graphs = {}


def create(type, usr):
    if type == 'doi':
        root = load_doi()
        root.addCloneSubGraph("graph")
        trace = root.addSubGraph("trace")
        graphs[usr] = root
        return trace


def load(trace_id):
    # todo load trace
    step = 0
    return tlp.loadGraph("data/" + trace_id + ".tlpb"), step


def save(trace_id):
    # todo save and destroy trace
    tlp.saveGraph("data/" + trace_id + ".tlpb")


def add_step(data):
    # load graph
    root = graphs[data['userId']]
    graph = root.getSubGraph("graph")
    trace = root.getSubGraph("trace")
    # add a Step
    newNode = trace.addNode()
    label = trace.getStringProperty("name")
    color = trace.getColorProperty("viewColor")
    layout = trace.getStringProperty("layout")
    size = trace.getIntegerProperty("doi_size")
    selection = trace.getStringProperty("selection")
    type = trace.getStringProperty("type")

    label[newNode] = "step " + str(newNode.id)
    layout[newNode] = data['layout']
    size[newNode] = data['size']
    selection[newNode] = str(list(data['selection'].values()))
    type[newNode] = data['type']

    # trace the edge and label it
    if data['actual'] != None:
        for n in trace.nodes():
            color[n] = tlp.Color(255, 95, 95)
            if str(n.id) == str(data['actual']):
                edge = trace.addEdge(n, newNode)
                edge_label = ""
                if layout[n] != layout[newNode]:
                    edge_label += layout[newNode]
                if selection[n] != selection[newNode]:
                    edge_label += " selection"
                if size[n] != size[newNode]:
                    size = size[newNode] - size[n]
                    if size > 0:
                        edge_label += " size +" + str(size)
                    else:
                        edge_label += " size " + str(size)
                if type[n] != type[newNode]:
                    edge_label += " " + type[newNode]
                label[edge] = edge_label

    color[newNode] = tlp.Color(20, 20, 255)
    params = tlp.getDefaultPluginParameters('Tree Leaf', trace)
    params['orientation'] = "right to left"
    trace.applyLayoutAlgorithm("Tree Leaf", trace.getLayoutProperty("viewLayout"), params)
    # apply DOI
    computeDoi = ComputeDoi(graph)
    result = computeDoi.create(list(data['selection'].values()), data['size'], str(newNode.id))
    view_selection = result.getBooleanProperty('viewSelection')
    view_selection.setAllEdgeValue(False)
    view_selection.setAllNodeValue(False)
    for n in result.nodes():
        if str(n.id) in list(data['selection'].values()):
            view_selection[n] = True
    params = tlp.getDefaultPluginParameters(data['layout'], result)
    result.applyLayoutAlgorithm(data['layout'], result.getLayoutProperty("viewLayout"), params)
    # tlp.saveGraph(result, "data/tlp/save.tlp")
    return trace, result, str(newNode.id)
