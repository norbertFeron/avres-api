import configparser
import os
import json

from flask_restful import Resource, reqparse
from flask import request
from routes.utils import makeResponse, getJson, applyLayout
from tulip import tlp

config = configparser.ConfigParser()
config.read("config.ini")

parser = reqparse.RequestParser()


class GetLayoutAlgorithm(Resource):
    def get(self):
        # return makeResponse(tlp.getLayoutAlgorithmPluginsList(), 200)
        list = ['FM^3 (OGDF)', 'Circular (OGDF)',  'Balloon (OGDF)',  'Sugiyama (OGDF)', 'Tree Leaf']
        return makeResponse(list, 200)


class drawGraph(Resource):
    def post(self, layout):
        graph = json.loads(request.data.decode("utf-8"))
        tulip_graph = tlp.newGraph()
        tulip_graph.setName('graph-ryder-draw')
        viewLayout = tulip_graph.getLayoutProperty("viewLayout")
        nodes = {}
        for n in graph['nodes']:
            node = tulip_graph.addNode()
            nodes[n['id']] = node
        for e in graph['edges']:
            tulip_graph.addEdge(nodes[e['source']], nodes[e['target']])
        applyLayout(tulip_graph, layout)
        for n in graph['nodes']:
            coord = viewLayout.getNodeStringValue(nodes[n['id']])[1:-1].split(',')
            n["x"] = float(coord[0])
            n["y"] = float(coord[1])
        print(graph)
        return makeResponse(graph, 200)
