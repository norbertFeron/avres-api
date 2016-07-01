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
        req += "OPTIONAL MATCH (find)-[:COMMENTS]->(post:post) "
        req += "RETURN find, author.uid AS author_id, author.name AS author_name, post.pid AS post_id, post.title AS post_title"
        result = neo4j.query_neo4j(req)
        author = {}
        post = {}
        for record in result:
            comment = record['find'].properties
            try:
                if record['author_id']:
                    author['uid'] = record['author_id']
            except KeyError:
                pass
            try:
                if record['author_name']:
                    author['name'] = record['author_name']
            except KeyError:
                pass
            try:
                if record['post_id']:
                    post['pid'] = record['post_id']
            except KeyError:
                pass
            try:
                if record['post_title']:
                    post['title'] = record['post_title']
            except KeyError:
                pass
        try:
            comment
        except NameError:
            return "ERROR : Cannot find post with pid: %d" % comment_id, 200
        comment['author'] = author
        comment['post'] = post
        return makeResponse([comment], 200)


class GetComments(Resource):
    def get(self):
        req = "MATCH (c:comment) RETURN c.cid AS cid, c.subject AS subject"
        req += addargs()
        result = neo4j.query_neo4j(req)
        comments = []
        for record in result:
            comments.append({'cid': record['cid'], "subject": record['subject']})
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
        req = "MATCH (c:comment)-[:COMMENTS]->(post:post { pid: %d}) RETURN c" % post_id
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
