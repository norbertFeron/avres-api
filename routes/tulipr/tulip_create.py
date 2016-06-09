import configparser
import os
import uuid

from flask_restful import Resource, reqparse
from routes.utils import makeResponse
from graphtulip.createtlp import CreateTlp
from tulip import *

config = configparser.ConfigParser()
config.read("config.ini")

parser = reqparse.RequestParser()


class CreateGraph(Resource):
    def get(self, field, value):
        graph_id = uuid.uuid4()
        creator = CreateTlp()
        creator.create(field, value, graph_id)
        return makeResponse([graph_id.urn[9:]])
