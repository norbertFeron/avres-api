from flask_restful import Resource
from neo4j.v1 import ResultError
from connector import neo4j
from routes.utils import addargs, makeResponse


class GetUser(Resource):
    def get(self, user_id):
        req = "MATCH (find:user {uid: %d}) RETURN find" % user_id
        result = neo4j.query_neo4j(req)
        try:
            return makeResponse([result.single()['find'].properties], 200)
        except ResultError:
            return makeResponse("ERROR : Cannot find user with uid: %d" % user_id, 204)


class GetUserHydrate(Resource):
    def get(self, user_id):
        req = "MATCH (find:user {uid: %d})" % user_id
        req += "OPTIONAL MATCH (find)-[:AUTHORSHIP]->(p:post)"
        req += "OPTIONAL MATCH (find)-[:AUTHORSHIP]->(c:comment)"
        req += "RETURN find, p, c"
        result = neo4j.query_neo4j(req)
        posts = []
        comments = []
        for record in result:
            user = record['find'].properties
            try:
                if record['p']:
                    posts.append(record['p'].properties)
                if record['c']:
                    comments.append(record['c'].properties)
            except KeyError:
                pass
        try:
            user
        except NameError:
            return makeResponse("ERROR : Cannot find post with pid: %d" % user_id, 204)
        user['posts'] = posts
        user['comments'] = comments
        return makeResponse([user], 200)


class GetUsers(Resource):
    def get(self):
        req = "MATCH (find:user) RETURN find"
        req += addargs()
        result = neo4j.query_neo4j(req)
        users = []
        for record in result:
            users.append(record['find'].properties)
        return makeResponse(users, 200)

