from flask_restful import Resource, reqparse
from neo4j.v1 import ResultError
from connector import neo4j
from routes.utils import addargs, addTimeFilter, makeResponse

parser = reqparse.RequestParser()


class GetPost(Resource):
    """
    @api {get} /post/:id Get post
    @apiName GetPost
    @apiGroup Post

    @apiParam {Number} id Post unique ID.

    @apiSuccess {Json} object The post.
    """
    def get(self, post_id):
        result = neo4j.query_neo4j("MATCH (find:post {pid: %d}) RETURN find" % post_id)
        try:
            return makeResponse(result.single()['find'].properties, 200)
        except ResultError:
            return makeResponse("ERROR : Cannot find post with pid: %d" % post_id, 204)


class GetPostHydrate(Resource): # todo comments on comments (with author)
    """
    @api {get} /post/hydrate/:id Get post + author/comments
    @apiName GetPostHydrate
    @apiGroup Post
    @apiDescription Get post info and his author/comments list

    @apiParam {Number} id post unique ID.

    @apiSuccess {Json} object The post.
    """
    def get(self, post_id):
        req = "MATCH (find:post {pid: %d}) " % post_id
        req += "OPTIONAL MATCH (find)<-[:AUTHORSHIP]-(author:user) "
        req += "OPTIONAL MATCH (find)<-[:COMMENTS]-(comment:comment) "
        req += "OPTIONAL MATCH (comment)<-[:AUTHORSHIP]-(commentAuthor:user) "
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
    """
    @api {get} /posts/?limit=:limit&orderBy:order Get posts
    @apiName GetPosts
    @apiGroup Post
    @apiDescription Get all post

    @apiParam {Number} [limit] Array size limit
    @apiParam {String} [order=uid:desc] "field:[desc|asc]"

    @apiSuccess {Json} array Posts list.
    """
    def get(self):
        req = "MATCH (p:post) RETURN p.pid AS pid, p.title AS title"
        req += addargs()
        result = neo4j.query_neo4j(req)
        posts = []
        for record in result:
            posts.append({'pid': record['pid'], "title": record['title']})
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
        parser.add_argument('uid', action='append')
        args = parser.parse_args()

        if args['uid']:
            req = "MATCH (n:post_type)<-[r:TYPE_IS]-(p:post) "
            req += addTimeFilter()
            for user in args['uid']:
                req += "OPTIONAL MATCH (n)<-[r%s:TYPE_IS]-(p:post)<-[]-(u%s:user {uid: %s}) " % (user, user, user)
            req += "RETURN n, count(r) AS nb_posts"
            for user in args['uid']:
                req += ", count(r%s) AS u%s_posts" % (user, user)
        else:
            req = "MATCH (n:post_type)<-[r:TYPE_IS]-(p:post) "
            req += addTimeFilter()
            req += "RETURN n, count(r) AS nb_posts"
        result = neo4j.query_neo4j(req)
        labels = []
        data = [[]]
        if args['uid']:
            for user in args['uid']:
                data.append([])
        for record in result:
            labels.append(record['n'].properties['name'])
            data[0].append(record['nb_posts'])
            if args['uid']:
                count = 1
                for user in args['uid']:
                    data[count].append(record['u%s_posts' % user])
                    count += 1
        return makeResponse({'labels': labels, 'data': data}, 200)
