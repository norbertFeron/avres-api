from flask_restful import Resource
from neo4j.v1 import ResultError
from connector import neo4j
from routes.utils import addargs


class GetPost(Resource):
    def get(self, post_id):
        result = neo4j.query_neo4j("MATCH (find:post {pid: %d}) RETURN find" % post_id)
        try:
            return result.single()['find'].properties, 200
        except ResultError:
            return "ERROR : Cannot find post with pid: %d" % post_id, 200


class GetPostHydrate(Resource): # todo comments on comments (with author)
    def get(self, post_id):
        req = "MATCH (find:post {pid: %d}) " % post_id
        req += "OPTIONAL MATCH (find)<-[:AUTHORSHIP]-(author:user) "
        req += "OPTIONAL MATCH (find)<-[:COMMENTS]-(comment:comment) "
        req += "OPTIONAL MATCH (find)<-[:AUTHORSHIP]-(commentAuthor:user) "
        req += "RETURN find, author, comment, commentAuthor"
        result = neo4j.query_neo4j(req)
        comments = []
        author = None
        for record in result:
            post = record['find'].properties
            try:
                if record['author']:
                    author = record['author'].properties
                if record['comment']:
                    comment = record['comment'].properties
                    if record['commentAuthor']:
                        comment['author'] = record['commentAuthor'].properties
                    comments.append(comment)
            except KeyError:
                pass
        try:
            post
        except NameError:
            return "ERROR : Cannot find post with pid: %d" % post_id, 200
        post['comments'] = comments
        post['author'] = author
        return post, 200


class GetPosts(Resource):
    def get(self):
        req = "MATCH (find:post) RETURN find"
        req += addargs()
        result = neo4j.query_neo4j(req)
        posts = []
        for record in result:
            posts.append(record['find'].properties)
        return posts


class GetPostsByType(Resource):
    def get(self, post_type):
        req = "MATCH (find:post {type: '%s'}) RETURN find" % post_type
        req += addargs()
        result = neo4j.query_neo4j(req)
        posts = []
        for record in result:
            posts.append(record['find'].properties)
        return posts


class GetPostsByAuthor(Resource):
    def get(self, author_id):
        req = "MATCH (author:user {uid: %d})-[:AUTHORSHIP]->(p:post) RETURN p" % author_id
        req += addargs()
        result = neo4j.query_neo4j(req)
        posts = []
        for record in result:
            posts.append(record['p'].properties)
        return posts


class GetPostType(Resource):
    def get(self):
        req = "" # todo
        result = neo4j.query_neo4j(req)
        types = []
        for record in result:
            types.append(record['type'])
        return types
