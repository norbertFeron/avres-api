from routes.tulipr.tulip_layout import GetLayoutAlgorithm, DrawCompleteGraph, DrawGraph
from routes.tulipr.tulip_create import CreateGraph
from routes.tulipr.tulip_doi import ComputeDOI


def add_tulip_routes(api):
    api.add_resource(GetLayoutAlgorithm, '/layoutAlgorithm')

    api.add_resource(CreateGraph, '/createGraph/<string:field>/<int:value>')

    api.add_resource(DrawCompleteGraph, '/drawComplete/<string:layout>')
    api.add_resource(DrawGraph, '/draw/<string:graph_id>/<string:layout>')

    api.add_resource(ComputeDOI, '/doi/<string:interest>')
