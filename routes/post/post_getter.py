from flask_restful import Resource
from neo4j.v1 import ResultError
from connector import neo4j
from routes.utils import addargs, makeResponse


class GetPost(Resource):
    def get(self, post_id):
        result = neo4j.query_neo4j("MATCH (find:post {pid: %d}) RETURN find" % post_id)
        try:
            return makeResponse([result.single()['find'].properties], 200)
        except ResultError:
            return makeResponse("ERROR : Cannot find post with pid: %d" % post_id, 204)


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
        return makeResponse(post, 200)


class GetPosts(Resource):
    def get(self):
        req = "MATCH (find:post) RETURN find"
        req += addargs()
        result = neo4j.query_neo4j(req)
        posts = []
        for record in result:
            posts.append(record['find'].properties)
        return makeResponse(posts, 200)


class GetPostsByType(Resource):
    def get(self, post_type):
        req = "MATCH (find:post {type: '%s'}) RETURN find" % post_type
        req += addargs()
        result = neo4j.query_neo4j(req)
        posts = []
        for record in result:
            posts.append(record['find'].properties)
        return makeResponse(posts, 200)


class GetPostsByAuthor(Resource):
    def get(self, author_id):
        req = "MATCH (author:user {uid: %d})-[:AUTHORSHIP]->(p:post) RETURN p" % author_id
        req += addargs()
        result = neo4j.query_neo4j(req)
        posts = []
        for record in result:
            posts.append(record['p'].properties)
        return makeResponse(posts, 200)


class GetPostType(Resource):
    def get(self):
        # todo add optional userId  to count <-[]-(u:user {uid: })
        req = "MATCH (n:post_type)<-[r:TYPE_IS]-(p:post)  RETURN n, count(r) AS nb_posts"
        result = neo4j.query_neo4j(req)
        labels = []
        data = [[]]
        for record in result:
            labels.append(record['n'].properties['name'])
            data[0].append(record['nb_posts'])
        return makeResponse([{'labels': labels, 'data': data}], 200)
