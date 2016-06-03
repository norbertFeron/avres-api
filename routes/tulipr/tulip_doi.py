from flask_restful import Resource
from tulip import *


class ComputeDOI(Resource):
    def get(self, interest):
        # todo compute doi
        return "ERROR : Cannot proceed DOI with interest : %s " % interest, 200
