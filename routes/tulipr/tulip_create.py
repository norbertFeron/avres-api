import uuid
import configparser
import os
import time
from flask_restful import Resource, reqparse
from routes.utils import makeResponse, getJson, getHtml, makeHtmlResponse
from graphtulip.createtlp import CreateTlp


config = configparser.ConfigParser()
config.read("config.ini")

parser = reqparse.RequestParser()
parser.add_argument('layout')
parser.add_argument('format')
parser.add_argument('label_key_left')
parser.add_argument('label_key_right')


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
       @apiParam {String} label first label
       @apiParam {String} edge edge between
       @apiParam {String} label second label
       @apiParam {String} layout tulip layout algorithm to apply
       @apiParam {String} label_key_left key of the property to field label field of the left node
       @apiParam {String} label_key_right key of the property to field label field of the right node
       @apiSuccess {Graph} Graph in json format.
    """
    def get(self, label1, edge, label2):
        creator = CreateTlp()
        params = (label1, edge, label2, parser.parse_args())
        graph = creator.createLabelEdgeLabel(params)
        args = parser.parse_args()
        if not args['layout']:
            args['layout'] = config['api']['default_layout']
        graph.applyLayoutAlgorithm(args['layout'])
        if args['format'] == 'html':
            return makeHtmlResponse(getHtml(graph), 200)
        else:
            return makeResponse(getJson(graph), 200)

class GetGraphNeighboursById(Resource):
    """
       @api {get} /getGraphNeighboursById/:id/:edge get neighbours graph with id and edge type 
       @apiName getGraphNeighboursById
       @apiGroup Graphs
       @apiDescription Get neighbours graph with id / edge type
       @apiParam {String} edge edge between
       @apiParam {String} layout tulip layout algorithm to apply
       @apiSuccess {Graph} Graph in json format.
    """
    def get(self, id, edge):
        creator = CreateTlp()
        params = (id, edge, parser.parse_args())
        graph = creator.createNeighboursById(params)
        args = parser.parse_args()
        if not args['layout']:
            args['layout'] = config['api']['default_layout']
        graph.applyLayoutAlgorithm(args['layout'])
        if args['format'] == 'html':
            return makeHtmlResponse(getHtml(graph), 200)
        else:
            return makeResponse(getJson(graph), 200)

