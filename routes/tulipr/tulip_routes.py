from routes.tulipr.tulip_create import *
from routes.tulipr.tulip_layout import GetLayoutAlgorithm, DrawGraph
from routes.tulipr.tulip_compute import ComputeDOI



def add_tulip_routes(api):

    gid_stack = {}

    # Generate
    api.add_resource(GenerateFullGraph, '/generateFullGraph', resource_class_kwargs={'gid_stack': gid_stack })
    api.add_resource(GenerateUserGraph, '/generateUserGraph', resource_class_kwargs={'gid_stack': gid_stack })
    api.add_resource(GenerateGraphWithoutUser, '/generateCommentAndPostGraph', resource_class_kwargs={'gid_stack': gid_stack })
    api.add_resource(GenerateGraphs, '/generateGraphs', resource_class_kwargs={'gid_stack': gid_stack })

    # Create
    api.add_resource(CreateGraph, '/createGraph/<string:field>/<int:value>', resource_class_kwargs={'gid_stack': gid_stack })
    api.add_resource(CreateGraphWithParams, '/createGraph', resource_class_kwargs={'gid_stack': gid_stack })
    api.add_resource(CreateGraphWithout, '/createGraphWithout', resource_class_kwargs={'gid_stack': gid_stack })

    # Layout
    api.add_resource(GetLayoutAlgorithm, '/layoutAlgorithm')
    api.add_resource(DrawGraph, '/draw/<string:public_gid>/<string:layout>', resource_class_kwargs={'gid_stack': gid_stack })

    # Compute
    api.add_resource(ComputeDOI, '/doi/<string:graph>/<string:type>/<int:id>', resource_class_kwargs={'gid_stack': gid_stack })

