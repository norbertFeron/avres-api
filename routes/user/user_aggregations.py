from flask_restful import Resource, reqparse
from neo4j.v1 import ResultError
from connector import neo4j
from routes.utils import addargs, makeResponse

parser = reqparse.RequestParser()


class CountUsersByTimestamp(Resource):
    def get(self):
        req = "MATCH (n:user) RETURN n.timestamp AS timestamp ORDER BY timestamp ASC"
        req += addargs()
        result = neo4j.query_neo4j(req)
        users = []
        count = 1
        for record in result:
            users.append({"count": count, "timestamp": record['timestamp']})
            count += 1
        return makeResponse(users, 200)
