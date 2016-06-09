from flask_restful import Resource
from neo4j.v1 import ResultError
from connector import neo4j
from routes.utils import addargs, makeResponse


class GetComment(Resource):
    def get(self, comment_id):
        req = "MATCH (find:comment {cid: %d}) RETURN find" % comment_id
        result = neo4j.query_neo4j(req)
        try:
            return makeResponse([result.single()['find'].properties], 200)
        except ResultError:
            return makeResponse("ERROR : Cannot find comment with cid: %d" % comment_id, 204)


class GetCommentHydrate(Resource):
    def get(self, comment_id):
        req = "MATCH (find:comment {cid: %d}) " % comment_id
        req += "OPTIONAL MATCH (find)<-[:AUTHORSHIP]-(author:user) "
        req += "OPTIONAL MATCH (find)<-[:COMMENTS]-(otherComment:comment) "
        req += "OPTIONAL MATCH (otherComment)<-[:AUTHORSHIP]-(otherCommentAuthor:user) "
        req += "RETURN find, author, otherComment, otherCommentAuthor"
        result = neo4j.query_neo4j(req)
        comments = []
        author = None
        other_comment = None
        for record in result:
            comment = record['find'].properties
            try:
                if record['author']:
                    author = record['author'].properties
            except KeyError:
                pass
            try:
                if record['otherComment']:
                    other_comment = record['otherComment'].properties
                    try:
                        if record['otherCommentAuthor']:
                            other_comment['author'] = record['otherCommentAuthor'].properties
                    except KeyError:
                        pass
                    comments.append(other_comment)
            except KeyError:
                pass
        try:
            comment
        except NameError:
            return "ERROR : Cannot find post with pid: %d" % comment_id, 200
        comment['comments'] = comments
        comment['author'] = author
        return makeResponse([comment], 200)


class GetComments(Resource):
    def get(self):
        req = "MATCH (find:comment) RETURN find"
        req += addargs()
        result = neo4j.query_neo4j(req)
        comments = []
        for record in result:
            comments.append(record['find'].properties)
        return makeResponse(comments, 200)


class GetCommentsByAuthor(Resource):
    def get(self, author_id):
        req = "MATCH (author:user {uid: %d})-[:AUTHORSHIP]->(c:comment) RETURN c" % author_id
        req += addargs()
        result = neo4j.query_neo4j(req)
        comments = []
        for record in result:
            comments.append(record['c'].properties)
        return makeResponse(comments, 200)


class GetCommentsOnPost(Resource):
    def get(self, post_id):
        req = "MATCH (c:comment)-[:COMMENTS]->(post:post { nid: %d}) RETURN c" % post_id # todo restructure maybe change nid
        req += addargs()
        result = neo4j.query_neo4j(req)
        comments = []
        for record in result:
            comments.append(record['c'].properties)
        return makeResponse(comments, 200)


class GetCommentsOnComment(Resource):
    def get(self, comment_id):
        req = "MATCH (c:comment)-[:COMMENTS]->(comment:comment { cid: %d}) RETURN c" % comment_id
        req += addargs()
        result = neo4j.query_neo4j(req)
        comments = []
        for record in result:
            comments.append(record['c'].properties)
        return makeResponse(comments, 200)
