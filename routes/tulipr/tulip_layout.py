from flask_restful import Resource, reqparse
from flask import send_file
import configparser
from tulip import *

config = configparser.ConfigParser()
config.read("config.ini")

parser = reqparse.RequestParser()


class GetLayoutAlgorithm(Resource):
    def get(self):
        return tlp.getLayoutAlgorithmPluginsList()


class DrawCompleteGraph(Resource):
    def get(self, layout):
        tulip_graph = tlp.loadGraph("%s%s.tlp" % (config['exporter']['tlp_path'], "complete"))
        # tulip_graph.applyLayoutAlgorithm(layout)
        path = "%s%s.json" % (config['exporter']['json_path'], "complete")
        tlp.exportGraph("SIGMA JSON Export", tulip_graph, path)
        return send_file(path)
