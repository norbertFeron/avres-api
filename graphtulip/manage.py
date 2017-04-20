from tulip import *
from loader.loader import load_doi

from graphtulip.degreeOfInterest import ComputeDoi

graphs = {}


def create(type, room):
    if type == 'doi':
        if room in graphs.keys():
            trace = graphs[room].getSubGraph('trace')
        else:
            root = load_doi()
            root.addCloneSubGraph("graph")
            trace = root.addSubGraph("trace")
            graphs[room] = root
        return trace


def load(trace_id):
    # todo load trace
    step = 0
    return tlp.loadGraph("data/" + trace_id + ".tlpb"), step


def getStep(room, step):
    graph = graphs[room].getSubGraph('graph')
    return graph.getSubGraph(str(step))


def save(trace_id):
    # todo save and destroy trace
    tlp.saveGraph("data/" + trace_id + ".tlpb")


def addStep(data):
    # load graph
    root = graphs[data['room']]
    graph = root.getSubGraph("graph")
    trace = root.getSubGraph("trace")
    # add a Step
    newNode = trace.addNode()
    label = trace.getLocalStringProperty("name")
    color = trace.getLocalColorProperty("viewColor")
    layout = trace.getLocalStringProperty("layout")
    size = trace.getLocalIntegerProperty("doi_size")
    selection = trace.getLocalStringProperty("selection")
    type = trace.getLocalStringProperty("type")

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
    trace.applyLayoutAlgorithm("Tree Leaf", trace.getLocalLayoutProperty("viewLayout"), params)
    # apply DOI
    computeDoi = ComputeDoi(graph)
    result = computeDoi.create(list(data['selection'].values()), data['size'], str(newNode.id))
    view_selection = result.getLocalBooleanProperty('viewSelection')
    view_selection.setAllEdgeValue(False)
    view_selection.setAllNodeValue(False)
    for n in result.nodes():
        if str(n.id) in list(data['selection'].values()):
            view_selection[n] = True
    params = tlp.getDefaultPluginParameters(data['layout'], result)
    # tlp.saveGraph(result, "data/tlp/save.tlpb")
    result.applyLayoutAlgorithm(data['layout'], result.getLocalLayoutProperty("viewLayout"), params)
    return trace, result, str(newNode.id)
