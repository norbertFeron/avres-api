from tulip import *


def create_trace(initial_step):
    trace = tlp.newGraph()
    add_step(trace, None, initial_step)
    return trace


def load_trace(trace_id):
    # todo load trace
    return tlp.loadGraph("data/treeExample.tlpb")


def add_step(trace, current_id, new):
    newNode = trace.addNode()
    nodeLabel = trace.getStringProperty("name")
    nodeColor = trace.getColorProperty("viewColor")
    if current_id != None:
        nodes = trace.getNodes()
        for n in nodes:
            nodeColor[n] = tlp.Color(255, 95, 95)
            if n.id == current_id:
                trace.addEdge(n, newNode)
    nodeLabel[newNode] = new
    nodeColor[newNode] = tlp.Color(20, 20, 255)
    params = tlp.getDefaultPluginParameters('Tree Leaf', trace)
    params['orientation'] = "right to left"
    trace.applyLayoutAlgorithm("Tree Leaf", trace.getLayoutProperty("viewLayout"), params)
    return newNode.id
