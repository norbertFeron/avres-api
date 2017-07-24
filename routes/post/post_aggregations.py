from flask_restful import Resource, reqparse
from neo4j.v1 import ResultError
from connector import neo4j
from routes.utils import addargs, makeResponse

parser = reqparse.RequestParser()


class CountAllPost(Resource):
    """
    @api {get} /posts/count/ Count posts
    @apiName CountAllPost
    @apiGroup Post
    @apiDescription Count all posts

    @apiSuccess {Number} Number of posts.
    """
    def get(self):
        req = "MATCH (:post) RETURN count(*) AS nb_posts"
        result = neo4j.query_neo4j(req)
        try:
            return makeResponse(result.single()['nb_posts'], 200)
        except ResultError:
            return makeResponse("ERROR", 500)


class CountPostByAuthor(Resource):
    """
    @api {get} /posts/count/author/:author_id Count posts by author
    @apiName CountPostByAuthor
    @apiGroup Post
    @apiDescription Count posts by author

    @apiParam {Number} author_id Author id

    @apiSuccess {Number} Number of posts.
    """
    def get(self, author_id):
        req = "MATCH (author:user {uid : %d})-[:AUTHORSHIP]->(:post) RETURN count(*) AS nb_posts" % author_id
        result = neo4j.query_neo4j(req)
        try:
            return makeResponse(result.single()['nb_posts'], 200)
        except ResultError:
            return makeResponse("ERROR", 500)


class CountPostsByTimestamp(Resource):
    """
    @api {get} /posts/count/timestamp Count Posts by time
    @apiName CountPostsByTimestamp
    @apiGroup Post
    @apiDescription Count all posts by timestamp

    @apiSuccess {Number} timestamp Timestamp of a step.
    @apiSuccess {Number} count Number of posts.

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
        req = "MATCH (n:post) RETURN n.timestamp AS timestamp ORDER BY timestamp ASC"
        req += addargs()
        result = neo4j.query_neo4j(req)
        posts = []
        count = 1
        for record in result:
            posts.append({"count": count, "timestamp": record['timestamp']})
            count += 1
        return makeResponse(posts, 200)
