import glob
from routes.tulipr.tulip_create import *
from routes.tulipr.tulip_layout import GetLayoutAlgorithm


def add_tulip_routes(api):

    # Create
    api.add_resource(GetRandomGraph, '/getGraph/random/')
    api.add_resource(GetGraphLabelEdgeLabel, '/getGraph/<string:label1>/<string:edge>/<string:label2>')
    api.add_resource(GetGraphNeighboursById, '/getGraphNeighboursById/<int:id>/<string:edge>/<string:label>')

    # Layout
    api.add_resource(GetLayoutAlgorithm, '/layoutAlgorithm')
