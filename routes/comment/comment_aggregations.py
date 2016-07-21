from flask_restful import Resource, reqparse
from neo4j.v1 import ResultError
from connector import neo4j
from routes.utils import addargs, makeResponse

parser = reqparse.RequestParser()


class CountAllComments(Resource):
    """
   @api {get} /comments/count/ Count comments
   @apiName CountAllComments
   @apiGroup Comment
   @apiDescription Count comments

   @apiSuccess {Number} Number of Comments.
   """
    def get(self):
        req = "MATCH (:comment) RETURN count(*) AS nb_comments"
        result = neo4j.query_neo4j(req)
        try:
            return makeResponse(result.single()['nb_comments'], 200)
        except ResultError:
            return makeResponse("ERROR", 500)


class CountCommentsByAuthor(Resource):
    """
    @api {get} /comments/count/author/:author_id Count comments by author
    @apiName CountCommentsByAuthor
    @apiGroup Comment
    @apiDescription Count comments by author

    @apiParam {Number} author_id Author id

    @apiSuccess {Number} Number of comments.
    """
    def get(self, author_id):
        req = "MATCH (author:user {uid : %d})-[:AUTHORSHIP]->(c:comment) RETURN count(*) AS nb_comments" % author_id
        result = neo4j.query_neo4j(req)
        try:
            return makeResponse(result.single()['nb_comments'], 200)
        except ResultError:
            return makeResponse("ERROR", 500)


class CountCommentsByTimestamp(Resource):
    """
    @api {get} /comments/count/timestamp Count comments by time
    @apiName CountCommentsByTimestamp
    @apiGroup Comments
    @apiDescription Count all comments by timestamp

    @apiSuccess {Number} timestamp Timestamp of a step.
    @apiSuccess {Number} count Number of comments.

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
        req = "MATCH (n:comment) RETURN n.timestamp AS timestamp ORDER BY timestamp ASC"
        req += addargs()
        result = neo4j.query_neo4j(req)
        comments = []
        count = 1
        for record in result:
            comments.append({"count": count, "timestamp": record['timestamp']})
            count += 1
        return makeResponse(comments, 200)
