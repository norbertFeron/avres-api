from routes.tulipr.tulip_layout import GetLayoutAlgorithm
from routes.tulipr.tulip_layout import DrawCompleteGraph
from routes.tulipr.tulip_doi import ComputeDOI


def add_tulip_routes(api):
    api.add_resource(GetLayoutAlgorithm, '/layoutAlgorithm/')
    api.add_resource(DrawCompleteGraph, '/drawComplete/<string:layout>')
    api.add_resource(ComputeDOI, '/doi/<string:interest>')
