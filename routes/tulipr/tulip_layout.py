from flask_restful import Resource, reqparse
from flask import send_file
import configparser
from tulip import *
import exportsigma

config = configparser.ConfigParser()
config.read("config.ini")

parser = reqparse.RequestParser()


class GetLayoutAlgorithm(Resource):
    def get(self):
        return tlp.getLayoutAlgorithmPluginsList()


class DrawCompleteGraph(Resource):
    def get(self, layout):
        tulip_graph = tlp.loadGraph(config['exporter']['tlp_path'])
        layout = "FM^3 (OGDF)"
        # todo why this crash python ?
        tulip_graph.applyLayoutAlgorithm(layout)
        path = "/Users/nferon/PycharmProjects/graph-ryder-api/data/tmp/complete.json"
        tlp.exportGraph("SIGMA JSON Export", tulip_graph, path)
        return send_file(path)
