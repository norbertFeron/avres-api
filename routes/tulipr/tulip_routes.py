from routes.tulipr.tulip_create import CreateGraph, CreateFullGraph
from routes.tulipr.tulip_layout import GetLayoutAlgorithm, DrawCompleteGraph, DrawGraph
from routes.tulipr.tulip_compute import ComputeDOI


def add_tulip_routes(api):

    # Create
    api.add_resource(CreateFullGraph, '/createFullGraph')
    api.add_resource(CreateGraph, '/createGraph/<string:field>/<int:value>')

    # Layout
    api.add_resource(GetLayoutAlgorithm, '/layoutAlgorithm')
    api.add_resource(DrawCompleteGraph, '/drawComplete/<string:layout>')
    api.add_resource(DrawGraph, '/draw/<string:graph_id>/<string:layout>')

    # Compute
    api.add_resource(ComputeDOI, '/doi/<string:type>/<int:id>')
