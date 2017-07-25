import glob
from routes.tulipr.tulip_create import *
from routes.tulipr.tulip_layout import GetLayoutAlgorithm, DrawGraph


def add_tulip_routes(api):

    # object use to stock {public_gid: private_gid} graph id
    gid_stack = {}

    # Create
    api.add_resource(CreateGraph, '/createGraph/<string:field>/<int:value>', resource_class_kwargs={'gid_stack': gid_stack })
    api.add_resource(CreateLabelEdgeLabel, '/createGraph/<string:label1>/<string:edge>/<string:label2>', resource_class_kwargs={'gid_stack': gid_stack})

    # Layout
    api.add_resource(GetLayoutAlgorithm, '/layoutAlgorithm')
    api.add_resource(DrawGraph, '/draw/<string:public_gid>/<string:layout>', resource_class_kwargs={'gid_stack': gid_stack })
