from flask_restful import reqparse
from flask import make_response
import json

parser = reqparse.RequestParser()
parser.add_argument('limit')
parser.add_argument('orderBy')
parser.add_argument('start')
parser.add_argument('end')


def addlimit():
    args = parser.parse_args()
    if args['limit']:
        return " LIMIT %s" % args['limit']
    else:
        return ''


def addorderby():
    args = parser.parse_args()
    if args['orderBy']:
        orderby = args['orderBy'].split(':')
        if len(orderby) > 1:
            return " ORDER BY n.%s %s" % (orderby[0], orderby[1])
        else:
            return " ORDER BY n.%s" % orderby[0]
    else:
        return ''


def addargs():
    req = addorderby()
    req += addlimit()
    return req


def addTimeFilter():
    args = parser.parse_args()
    req = ''
    if args['start']:
        req += "WHERE %s <= p.timestamp " % args['start']
    if args['start'] and args['end']:
        req += "AND %s >= p.timestamp " % args['end']
    if not args['start'] and args['end']:
        req += "WHERE %s >= p.timestamp " % args['end']
    return req


def makeResponse(result, code=200, file=False):
    if file:
        result = json.load(open(result, 'r', encoding="utf-8"))
    result = json.dumps(result)
    response = make_response(result, code)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    response.headers.add('Content-Type', 'application/json')
    return response


def getJson(graph):
    # edges
    edges = []
    for edge in graph.getEdges():
        # edge properties
        e = {"source": graph.source(edge).id, "target": graph.target(edge).id}
        for prop in graph.getObjectProperties():
            # edge color
            if prop.getName() == "viewColor":
                colors = prop.getEdgeStringValue(edge)[1:][:-1].split(',')
                e["color"] = 'rgb(' + colors[0] + ',' + colors[1] + ',' + colors[2] + ')'
            # edge label
            elif prop.getName() == "name":
                if prop.getEdgeStringValue(edge):
                    label = prop.getEdgeStringValue(edge).replace('"', '\\\"')
                    e["label"] = label
                    # else:
                    # json += '%s"label":"edge%s", %s' % (hr_2t, edge.id, hr_n)
            elif prop.getName() == "timestamp":
                if prop.getEdgeValue(edge):
                    e["timestamp"] = prop.getEdgeValue(edge)
            # other
            # elif prop.getEdgeDefaultStringValue() != prop.getEdgeStringValue(edge) \
            #         and prop.getEdgeStringValue(edge):
            #     value = prop.getEdgeStringValue(edge)\
            #         .replace('"', '\\\"')\
            #         .replace("\n", "\\n")\
            #         .replace("\r", "\\r")\
            #         .replace("\t", "\\t")
            #     e[prop.getName()] = value
        # sigma id
        e["id"] = edge.id
        e["type"] = 'arrow'
        edges.append(e)

    # nodes
    nodes = []
    for node in graph.getNodes():
        n = {}
        for prop in graph.getObjectProperties():
            # node color
            if prop.getName() == "viewColor":
                colors = prop.getNodeStringValue(node)[1:].split(',')
                n["color"] = 'rgb(' + colors[0] + ',' + colors[1] + ',' + colors[2] + ')'
            # node label
            elif prop.getName() == "name":
                if prop.getNodeStringValue(node):
                    label = prop.getNodeStringValue(node).replace('"', '\\\"')
                    n["label"] = label
                else:
                    n["label"] = "node" + str(node.id)
            # node size
            elif prop.getName() == "viewSize":
                size = prop.getNodeStringValue(node)[1:-1].split(',')
                size = (int(size[0]) + int(size[1])) / 2
                n["size"] = size
            # node layout
            elif prop.getName() == "viewLayout":
                coord = prop.getNodeStringValue(node)[1:-1].split(',')
                n["x"] = coord[0]
                n["y"] = float(coord[1]) * (-1)
            elif prop.getName() == "originalId":
                n["originalId"] = prop.getNodeValue(node)
            elif prop.getName() == "layout":
                n["layout"] = prop.getNodeStringValue(node)
            elif prop.getName() == "doi_size":
                n["doi_size"] = prop.getNodeValue(node)
            elif prop.getName() == "selection":
                n["selection"] = prop.getNodeStringValue(node)
            elif prop.getName() == "type":
                n["type"] = prop.getNodeStringValue(node)
            elif prop.getName() == "viewSelection":
                n["viewSelection"] = prop.getNodeValue(node)
            # other
            elif prop.getNodeDefaultStringValue() != prop.getNodeStringValue(node) \
                    and prop.getNodeStringValue(node):
                n[prop.getName()] = prop.getNodeStringValue(node)\
                    .replace('"', '\\\"')\
                    .replace("\n", "")\
                    .replace("\r", "")\
                    .replace("\t", "")
            # sigma id
        n["id"] = node.id
        if not n in nodes:
            nodes.append(n)
    return {"edges": edges, "nodes": nodes}

