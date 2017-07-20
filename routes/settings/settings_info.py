import psutil
from flask_restful import Resource
from routes.utils import makeResponse
from neo4j.v1 import ResultError
from connector import neo4j


class Info(Resource):
    def get(self):
        # todo change status if not ok
        response = {"status": "ok", "version": "0000000000000", "percentRamUsage": psutil.virtual_memory()[2], "percentDiskUsage": psutil.disk_usage('/')[3]}
        return makeResponse(response, 200)