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
        algos = tlp.getLayoutAlgorithmPluginsList()
        return makeResponse(algos, 200)


# todo remove old route
class DrawCompleteGraph(Resource):
    def get(self, layout):
        tulip_graph = tlp.loadGraph("%s%s.tlp" % (config['exporter']['tlp_path'], "complete"))
        tulip_graph.applyLayoutAlgorithm(layout)
        path = "%s%s.json" % (config['exporter']['json_path'], "complete")
        tlp.exportGraph("SIGMA JSON Export", tulip_graph, path)
        return makeResponse(path, 200, True)


class DrawGraph(Resource):
    def get(self, graph_id, layout):
        # check if the graph exist
        # todo change to a database with id -> filePath for security
        if not os.path.isfile("%s%s.tlp" % (config['exporter']['tlp_path'], graph_id)):
            return makeResponse("Unknow graph id : %d" % graph_id)
        tulip_graph = tlp.loadGraph("%s%s.tlp" % (config['exporter']['tlp_path'], graph_id))
        tulip_graph.applyLayoutAlgorithm(layout)
        path = "%s%s.json" % (config['exporter']['json_path'], graph_id)
        tlp.exportGraph("SIGMA JSON Export", tulip_graph, path)
        return makeResponse(path, 200, True)