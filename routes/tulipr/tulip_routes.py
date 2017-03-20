import glob
import os
import configparser

from routes.tulipr.tulip_layout import GetLayoutAlgorithm, DrawGraph
from routes.tulipr.tulip_compute import ComputeDOI

config = configparser.ConfigParser()
config.read("config.ini")


def add_tulip_routes(api):

    # object use to stock {public_gid: private_gid} graph id
    gid_stack = {}
    # clean tlp folder
    files = glob.glob("%s*" % config['exporter']['tlp_path'])
    for f in files:
        os.remove(f)

    # Layout
    api.add_resource(GetLayoutAlgorithm, '/layoutAlgorithm')
    api.add_resource(DrawGraph, '/draw/<string:public_gid>/<string:layout>', resource_class_kwargs={'gid_stack': gid_stack })

    # Compute
    api.add_resource(ComputeDOI, '/doi', resource_class_kwargs={'gid_stack': gid_stack })

