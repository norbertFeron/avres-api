from routes.tulipr.tulip_create import *
from routes.tulipr.tulip_layout import GetLayoutAlgorithm, DrawCompleteGraph, DrawGraph
from routes.tulipr.tulip_compute import ComputeDOI


def add_tulip_routes(api):

    # Generate
    api.add_resource(GenerateFullGraph, '/generateFullGraph')
    api.add_resource(GenerateUserGraph, '/generateUserGraph')
    api.add_resource(GenerateGraphWithoutUser, '/generateCommentAndPostGraph')
    api.add_resource(GenerateGraphs, '/generateGraphs')

    # Create
    api.add_resource(CreateGraph, '/createGraph/<string:field>/<int:value>')
    api.add_resource(CreateGraphWithParams, '/createGraph')
    api.add_resource(CreateGraphWithout, '/createGraphWithout')

    # Layout
    api.add_resource(GetLayoutAlgorithm, '/layoutAlgorithm')
    api.add_resource(DrawCompleteGraph, '/drawComplete/<string:layout>')
    api.add_resource(DrawGraph, '/draw/<string:graph_id>/<string:layout>')

    # Compute
    api.add_resource(ComputeDOI, '/doi/<string:graph>/<string:type>/<int:id>')