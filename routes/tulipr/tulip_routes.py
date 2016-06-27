from routes.tulipr.tulip_create import *
from routes.tulipr.tulip_layout import GetLayoutAlgorithm, DrawCompleteGraph, DrawGraph
from routes.tulipr.tulip_compute import ComputeDOI, ComputeUserDOI, ComputeSearchDOI


def add_tulip_routes(api):

    # Create (static)
    api.add_resource(CreateFullGraph, '/createFullGraph')
    api.add_resource(CreateUserGraph, '/createUserGraph')
    api.add_resource(CreateGraphWithoutUser, '/createCommentAndPostGraph')

    # Create
    api.add_resource(CreateGraph, '/createGraph/<string:field>/<int:value>')
    api.add_resource(CreateGraphWithParams, '/createGraph')
    api.add_resource(CreateGraphWithout, '/createGraphWithout')

    # Layout
    api.add_resource(GetLayoutAlgorithm, '/layoutAlgorithm')
    api.add_resource(DrawCompleteGraph, '/drawComplete/<string:layout>')
    api.add_resource(DrawGraph, '/draw/<string:graph_id>/<string:layout>')

    # Compute
    api.add_resource(ComputeDOI, '/doi/<string:type>/<int:id>')
    api.add_resource(ComputeSearchDOI, '/doi/<string:graph>/<string:type>/<int:id>')
    api.add_resource(ComputeUserDOI, '/users/doi/<string:type>/<int:id>')
