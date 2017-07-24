import configparser
import os
import tempfile

from flask_restful import Resource, reqparse
from routes.utils import makeResponse
from tulip import *

config = configparser.ConfigParser()
config.read("config.ini")

parser = reqparse.RequestParser()


class GetLayoutAlgorithm(Resource):
    """
    @api {get} /layoutAlgorithm Get layout
    @apiName GetLayoutAlgorithm
    @apiGroup Tulip
    @apiDescription Get list of tulip's layout algorithms

    @apiSuccess {Json} [String] list of algorithms.
    """
    def get(self):
        return makeResponse(tlp.getLayoutAlgorithmPluginsList(), 200)


class DrawGraph(Resource):
    """
    @api {get} /draw/:graph_id/:layout Draw graph
    @apiName DrawGraph
    @apiGroup Tulip
    @apiDescription Draw a graph with id and algorithm

    @apiParam {Number} id post unique ID.
    @apiParam {String} layout Draw algorithm.

    @apiExample {curl} Example usage:
    curl -i http://localhost:5000/draw/complete/FM^3%20(OGDF)

    @apiSuccess {Json} object The graph in json format.
    """
    def __init__(self, **kwargs):
        self.gid_stack = kwargs['gid_stack']

    def get(self, public_gid, layout):
        private_gid = self.gid_stack[public_gid]
        if not os.path.isfile("%s%s.tlp" % (config['exporter']['tlp_path'], private_gid)):
            return makeResponse("Unknow graph id : %s" % public_gid)
        tulip_graph = tlp.loadGraph("%s%s.tlp" % (config['exporter']['tlp_path'], private_gid))
        tulip_graph.applyLayoutAlgorithm(layout)
        path = tempfile.mkstemp()
        tlp.exportGraph("SIGMA JSON Export", tulip_graph, path[1])
        return makeResponse(path[1], 200, True)
