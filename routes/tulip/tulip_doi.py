from flask_restful import Resource
from neo4j.v1 import ResultError
from connector import neo4j
from tulip import *


class ComputeDOI(Resource):
    def get(self, interest):

        return "ERROR : Cannot proceed DOI with interest : " % interest, 200
