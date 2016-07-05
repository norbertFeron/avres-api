import configparser
import os

from flask_restful import Resource, reqparse
from routes.utils import makeResponse
from tulip import *

config = configparser.ConfigParser()
config.read("config.ini")

parser = reqparse.RequestParser()


class GetLayoutAlgorithm(Resource):
    def get(self):
        return makeResponse(tlp.getLayoutAlgorithmPluginsList(), 200)


class DrawGraph(Resource):
    def get(self, graph_id, layout):
        # check if the graph exist
        # todo change to a database with id -> filePath for security
        if not os.path.isfile("%s%s.tlp" % (config['exporter']['tlp_path'], graph_id)):
            return makeResponse("Unknow graph id : %s" % graph_id)
        tulip_graph = tlp.loadGraph("%s%s.tlp" % (config['exporter']['tlp_path'], graph_id))
        tulip_graph.applyLayoutAlgorithm(layout)
        path = "%s%s.json" % (config['exporter']['json_path'], graph_id)
        tlp.exportGraph("SIGMA JSON Export", tulip_graph, path)
        return makeResponse(path, 200, True)
