import configparser
import os

from flask_restful import Resource, reqparse
from routes.utils import makeResponse
from tulip import *

config = configparser.ConfigParser()
config.read("config.ini")

parser = reqparse.RequestParser()


class GetLayoutAlgorithm(Resource):
    def get(self):
        # return makeResponse(tlp.getLayoutAlgorithmPluginsList(), 200)
        list = ['FM^3 (OGDF)', 'Circular (OGDF)',  'Balloon (OGDF)',  'Sugiyama (OGDF)', 'Tree Leaf']
        return makeResponse(list, 200)
