import uuid
import configparser
import os
import time
from tulip import tlp
from flask_restful import Resource, reqparse, abort
from neo4j.v1.exceptions import CypherError
from routes.utils import makeResponse, getJson, getHtml, makeHtmlResponse, applyLayout
from graphtulip.createtlp import CreateTlp


config = configparser.ConfigParser()
config.read("config.ini")

parser = reqparse.RequestParser()
parser.add_argument('layout')
parser.add_argument('format')
parser.add_argument('depth')
parser.add_argument('label_key_left')
parser.add_argument('label_key_right')
parser.add_argument('label_key_edge')
parser.add_argument('color_left')
parser.add_argument('color_right')
parser.add_argument('color_edge')
parser.add_argument('query')


class GetRandomGraph(Resource):
    """
       @api {get} /getGraph/random/ get graph with ?
       @apiName getGraph Random
       @apiGroup Graphs
       @apiDescription Get a random graph
       @apiParam {layout} tulip layout algorithm to apply
       @apiSuccess {Graph} Graph in json format.
    """
    def get(self):
        creator = CreateTlp()
        params = []
        graph = creator.create(params)
        args = parser.parse_args()
        if args['layout']:
            applyLayout(graph, args['layout'])
        return makeResponse(getJson(graph), 200)


class GetQueryGraph(Resource):
    """
       @api {get} /getGraph/:query get graph with ?
       @apiName getGraph
       @apiGroup Graphs
       @apiDescription Get graph with a query
       @apiParam {value} query
       @apiParam {layout} tulip layout algorithm to apply
       @apiSuccess {Graph} Graph in json format.
    """
    def get(self):
        creator = CreateTlp()
        params = parser.parse_args()
        try:
            graph = creator.createGraphQuery(params)
        except (CypherError,  KeyError) as e:
           abort(400, description="Invalid request.")
        args = parser.parse_args()
        if len(graph.edges()) == 0:
            args['layout'] = 'Circular (OGDF)'
        applyLayout(graph, args['layout'])
        if args['format'] == 'html':
            return makeHtmlResponse(getHtml(graph), 200)
        else:
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
       @apiParam {String} format html for html quick preview
       @apiParam {String} label_key_left key of the property to field label field of the left node
       @apiParam {String} label_key_right key of the property to field label field of the right node
       @apiSuccess {Graph} Graph in json format.
    """
    def get(self, label1, edge, label2):
        creator = CreateTlp()
        params = (label1, edge, label2, parser.parse_args())
        graph = creator.createLabelEdgeLabel(params)
        args = parser.parse_args()
        applyLayout(graph, args['layout'])
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
        @apiParam {String} format html for html quick preview
        @apiParam {String} layout tulip layout algorithm to apply
        @apiSuccess {Graph} Graph in json format.
       @api {get} /getGraphNeighboursById/:id/:edge get neighbours graph with id and edge type 
       @apiName getGraphNeighboursById
       @apiGroup Graphs
       @apiDescription Get neighbours graph with id / edge type
       @apiParam {String} edge edge between
       @apiParam {String} layout tulip layout algorithm to apply
       @apiSuccess {Graph} Graph in json format.
    """
    def get(self, id, edge, label):
        creator = CreateTlp()
        params = (id, edge, label, parser.parse_args())
        graph = creator.createNeighboursById(params)
        args = parser.parse_args()
        if not args['layout']:
            args['layout'] = config['api']['default_layout']
        applyLayout(graph, args['layout'])
        if args['format'] == 'html':
            return makeHtmlResponse(getHtml(graph), 200)
        else:
            return makeResponse(getJson(graph), 200)
