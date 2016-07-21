from flask_restful import Resource, reqparse
from neo4j.v1 import ResultError
from connector import neo4j
from routes.utils import addargs, makeResponse

parser = reqparse.RequestParser()


class CountUsersByTimestamp(Resource):
    """
    @api {get} /users/count/timestamp Count users by time
    @apiName CountUsersByTimestamp
    @apiGroup User
    @apiDescription Count all users by timestamp

    @apiSuccess {Number} timestamp Timestamp of a step.
    @apiSuccess {Number} count Number of users.

    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        [{
            "timestamp": 1315749060000,
            "count": 1
        },
        {
            "timestamp": 1316199060000,
            "count": 2
        },
        {
            "timestamp": 1316351640000,
            "count": 3
        }]
    """
    def get(self):
        req = "MATCH (n:user) "
        req += "RETURN n.timestamp AS timestamp ORDER BY timestamp ASC"
        result = neo4j.query_neo4j(req)
        users = []
        count = 1
        for record in result:
            users.append({"count": count, "timestamp": record['timestamp']})
            count += 1
        return makeResponse(users, 200)
