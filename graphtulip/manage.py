import time
from tulip import *
from loader.loader import load_doi

from graphtulip.degreeOfInterest import ComputeDoi
from routes.utils import getJson

root = load_doi()
root.addCloneSubGraph("graph")
traces = []


def onJoin(type, room):
    if type == 'doi':
        if room in traces:
            trace = root.getSubGraph('trace' + room)
            if not trace.nodes():
                step = None
            else:
                step = trace.nodes()[-1].id
        else:
            trace = root.addSubGraph("trace" + room)
            traces.append(room)
            step = None
        return trace, step


def load(trace_id):
    # todo load trace
    return None, None


def getNodes():
    graph = root.getSubGraph('graph')
    name = graph.getStringProperty("name")
    type = graph.getStringProperty("type")
    labelsNodeTlp = graph.getStringVectorProperty("labelsNodeTlp")
    nodes = []
    for n in graph.getNodes():
        n_type = str(type.getNodeValue(n)) + str(labelsNodeTlp.getNodeValue(n))
        nodes.append({"name": name.getNodeValue(n), "type": n_type, "id": n.id})
    return nodes


def getStep(data):
    trace = root.getSubGraph("trace" + data['room'])
    graph = root.getSubGraph('graph')

    layout = trace.getLocalStringProperty("layout")
    size = trace.getLocalIntegerProperty("doi_size")
    selection = trace.getLocalStringProperty("selection")
    type = trace.getLocalStringProperty("type")

    step = {}

    for n in trace.nodes():
        if n.id == data['step']:
            step['layout'] = layout[n]
            step['size'] = size[n]
            step['selection'] = selection[n]
            step['type'] = type[n]
            step['id'] = n.id
    step['graph'] = getJson(graph.getSubGraph(str(data['step'])))

    return step


def save(trace_id):
    # todo save
    tlp.saveGraph("data/" + trace_id + ".tlpb")


# def add_annotation(data):
#     graph = root.getSubGraph("graph")
#     trace = root.getSubGraph("trace" + data['room'])
#     actual = graph.getSubGraph(str(data['step']))
#
#     name = graph.getStringProperty("name")
#     viewLayout = graph.getLayoutProperty("viewLayout")
#
#     annotation = actual.addNode()
#     name[annotation] = "annotation test"
#
#     # add self loop on trace
#
#     return trace, actual


def addStep(data):
    # Load graph
    graph = root.getSubGraph("graph")
    trace = root.getSubGraph("trace" + data['room'])

    label = trace.getLocalStringProperty("name")
    color = trace.getLocalColorProperty("viewColor")
    layout = trace.getLocalStringProperty("layout")
    timestamp = trace.getLocalIntegerProperty("timestamp")
    size = trace.getLocalIntegerProperty("doi_size")
    selection = trace.getLocalStringProperty("selection")
    type = trace.getLocalStringProperty("type")

    # Add a Step
    newNode = trace.addNode()
    label[newNode] = "step " + str(newNode.id)
    layout[newNode] = data['layout']
    type[newNode] = data['type']
    size[newNode] = data['size']
    selection[newNode] = str(data['selection'])

    if data['type'] == 'doi':
        # Trace the edge and label it
        if data['actual'] != None:
            for n in trace.nodes():
                if str(n.id) == str(data['actual']):
                    edge = trace.addEdge(n, newNode)
                    edge_label = ""
                    if layout[n] != layout[newNode]:
                        edge_label += layout[newNode]
                    if selection[n] != selection[newNode]:
                        # edge_label += " selection" + selection[newNode]
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
                    timestamp[edge] = int(time.time())

        computeDoi = ComputeDoi(graph)
        result = computeDoi.create(data['selection'], data['size'], str(newNode.id))
        view_selection = result.getLocalBooleanProperty('viewSelection')
        view_selection.setAllEdgeValue(False)
        view_selection.setAllNodeValue(False)
        for n in result.nodes():
            if n.id in data['selection']:
                view_selection[n] = True
    else:
        for n in trace.nodes():
            if n.id == data['actual']:
                edge = trace.addEdge(n, newNode)
                label[edge] = layout[newNode]
                timestamp[edge] = int(time.time())

        actual = graph.getSubGraph(str(data['actual']))
        result = actual.addCloneSubGraph(str(newNode.id), True, True)

    # Apply layout on the trace
    params = tlp.getDefaultPluginParameters('Tree Leaf', trace)
    # params = tlp.getDefaultPluginParameters('OrthoTree', trace)
    params['orientation'] = "right to left"
    trace.applyLayoutAlgorithm("Tree Leaf", trace.getLocalLayoutProperty("viewLayout"), params)
    # trace.applyLayoutAlgorithm("OrthoTree", trace.getLocalLayoutProperty("viewLayout"), params)

    # Apply color scale en edges  # todo reactivate when pip tulip 5.1 is ready
    # params = tlp.getDefaultPluginParameters('Color Mapping', trace)
    # colors = [tlp.Color.Blue, tlp.Color.Red]
    # colorScale = tlp.ColorScale(colors)
    # params['color scale'] = colorScale
    # params['input property'] = timestamp
    # params['target'] = "edges"
    # trace.applyColorAlgorithm('Color Mapping', params)

    # Apply layout on the graph
    params = tlp.getDefaultPluginParameters(data['layout'], result)
    result.applyLayoutAlgorithm(data['layout'], result.getLocalLayoutProperty("viewLayout"), params)
    tlp.saveGraph(root, "data/tlp/root.tlpb")
    return trace, newNode.id
