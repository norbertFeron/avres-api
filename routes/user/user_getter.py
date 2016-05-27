from flask_restful import Resource
from neo4j.v1 import ResultError
from connector import neo4j
from routes.utils import addargs


class GetUser(Resource):
    def get(self, user_id):
        req = "MATCH (find:user {uid: %d}) RETURN find" % user_id
        result = neo4j.query_neo4j(req)
        try:
            return result.single()['find'].properties, 200
        except ResultError:
            return "ERROR : Cannot find user with uid: %d" % user_id, 200  # todo create error code


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
            return "ERROR : Cannot find post with pid: %d" % user_id, 200
        user['posts'] = posts
        user['comments'] = comments
        return user, 200


class GetUsers(Resource):
    def get(self):
        req = "MATCH (find:user) RETURN find"
        req += addargs()
        result = neo4j.query_neo4j(req)
        users = []
        for record in result:
            users.append(record['find'].properties)
        return users


class GetShortestPathBetweenUsers(Resource):
    def get(self, user1_id, user2_id, max_hop):
        req = "MATCH path=shortestPath((u1:user {uid: %d})-[*..%d]-(u2:user {uid: %d}))RETURN path" % (
            user1_id, max_hop, user2_id)
        result = neo4j.query_neo4j(req)
        try:
            print(result.single()['path'])  # todo this is the path ?
            return 'I don\'t understand the result, sorry.', 200
        except ResultError:
            return "ERROR : Cannot find a path between uid: %d and uid: %d with maximum %d hop" % (
                user1_id, user2_id, max_hop), 200
