import uuid
import configparser
import os
import time
from flask_restful import Resource, reqparse
from routes.utils import makeResponse, getJson
from graphtulip.createtlp import CreateTlp


config = configparser.ConfigParser()
config.read("config.ini")

parser = reqparse.RequestParser()
parser.add_argument('layout')


class GetGraph(Resource):
    """
       @api {get} /getGraph/:field/:value get graph with ?
       @apiName getGraph
       @apiGroup Graphs
       @apiDescription Get graph with field/value
       @apiParam {String} field  ?
       @apiParam {value} value ?
       @apiParam {layout} tulip layout algorithm to apply
       @apiSuccess {Graph} Graph in json format.
    """
    def get(self, field, value):
        creator = CreateTlp()
        params = [(field, value)]
        graph = creator.create(params)
        args = parser.parse_args()
        if not args['layout']:
            args['layout'] = config['api']['default_layout']
        graph.applyLayoutAlgorithm(args['layout'])
        return makeResponse(getJson(graph), 200)


class GetGraphLabelEdgeLabel(Resource):
    """
       @api {get} /getGraph/:label/:edge/label get graph with pattern label-edge->label 
       @apiName getGraph
       @apiGroup Graphs
       @apiDescription Get graph with field/value
       @apiParam {String} field  ?
       @apiParam {value} value ?
       @apiParam {layout} tulip layout algorithm to apply
       @apiSuccess {Graph} Graph in json format.
    """
    def get(self, label1, edge, label2):
        creator = CreateTlp()
        params = (label1, edge, label2)
        graph = creator.createlabeledgelabel(params)
        args = parser.parse_args()
        if not args['layout']:
            args['layout'] = config['api']['default_layout']
        graph.applyLayoutAlgorithm(args['layout'])
        return makeResponse(getJson(graph), 200)

