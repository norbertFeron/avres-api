import uuid
import configparser
import os
import time
from flask_restful import Resource, reqparse
from routes.utils import makeResponse
from graphtulip.createtlp import CreateTlp
from graphtulip.createfulltlp import CreateFullTlp
from graphtulip.createusertlp import CreateUserTlp

config = configparser.ConfigParser()
config.read("config.ini")

parser = reqparse.RequestParser()

# Graph generate once


class GenerateFullGraph(Resource):
    """
    @api {get} /generateFullGraph Generate complete graph
    @apiName GenerateFullGraph
    @apiGroup Tulip
    @apiDescription Generate the full graph 'complete'

    @apiSuccess {Boolean} True or False.
    """
    def __init__(self, **kwargs):
        self.gid_stack = kwargs['gid_stack']

    def get(self):
        if 'complete' in self.gid_stack.keys():
            os.remove('%s%s.tlp' % (config['exporter']['tlp_path'], self.gid_stack.pop("complete")))
        private_gid = uuid.uuid4().urn[9:]
        creator = CreateFullTlp()
        creator.create(private_gid)
        self.gid_stack.update({"complete": private_gid})
        return makeResponse(True)


class GenerateUserGraph(Resource):
    """
    @api {get} /generateUserGraph Generate usersToUsers graph
    @apiName GenerateUserGraph
    @apiGroup Tulip
    @apiDescription Generate the users graph

    @apiSuccess {Boolean} True or False.
    """
    def __init__(self, **kwargs):
        self.gid_stack = kwargs['gid_stack']

    def get(self):
        if 'usersToUsers' in self.gid_stack.keys():
            os.remove('%s%s.tlp' % (config['exporter']['tlp_path'], self.gid_stack.pop("usersToUsers")))
        private_gid = uuid.uuid4().urn[9:]
        creator = CreateUserTlp()
        creator.create(private_gid)
        self.gid_stack.update({"usersToUsers": private_gid})
        return makeResponse(True)


class GenerateGraphWithoutUser(Resource):
    """
    @api {get} /generateCommentAndPostGraph Generate commentsAndPosts graph
    @apiName GenerateGraphWithoutUser
    @apiGroup Tulip
    @apiDescription Generate the commentsAndPosts graph

    @apiSuccess {Boolean} True or False.
    """
    def __init__(self, **kwargs):
        self.gid_stack = kwargs['gid_stack']

    def get(self):
        if 'commentAndPost' in self.gid_stack.keys():
            os.remove('%s%s.tlp' % (config['exporter']['tlp_path'], self.gid_stack.pop("commentAndPost")))
        private_gid = uuid.uuid4().urn[9:]
        creator = CreateTlp()
        creator.createWithout(["user"], private_gid)
        self.gid_stack.update({"commentAndPost": private_gid})
        return makeResponse(True)


class GenerateGraphs(Resource):
    """
    @api {get} /generateGraphs Generate static graphs
    @apiName generateGraphs
    @apiGroup Tulip
    @apiDescription Generate the 3 static graphs

    @apiSuccess {Boolean} True or False.
    """
    def __init__(self, **kwargs):
        self.gid_stack = kwargs['gid_stack']

    def get(self, returnValue=True):
        # Full graph
        if 'complete' in self.gid_stack.keys():
            os.remove('%s%s.tlp' % (config['exporter']['tlp_path'], self.gid_stack.pop("complete")))
        creator = CreateFullTlp()
        complete_gid = uuid.uuid4().urn[9:]
        creator.create(complete_gid)
        self.gid_stack.update({"complete": complete_gid})
        # User Graph
        if 'usersToUsers' in self.gid_stack.keys():
            os.remove('%s%s.tlp' % (config['exporter']['tlp_path'], self.gid_stack.pop("usersToUsers")))
        creator = CreateUserTlp()
        users_gid = uuid.uuid4().urn[9:]
        creator.create(users_gid)
        self.gid_stack.update({"usersToUsers": users_gid})
        # Comment And Post Graph
        if 'commentAndPost' in self.gid_stack.keys():
            os.remove('%s%s.tlp' % (config['exporter']['tlp_path'], self.gid_stack.pop("commentAndPost")))
        creator = CreateTlp()
        commentPost_gid = uuid.uuid4().urn[9:]
        creator.createWithout(["user"], commentPost_gid)
        self.gid_stack.update({"commentAndPost": commentPost_gid})
        if returnValue:
            return makeResponse(True)


# Create new graph


class CreateGraph(Resource):
    """
    @api {get} /createGraph/:field/:value Create a Graph
    @apiName CreateGraph
    @apiGroup Tulip
    @apiDescription Create a graph from type and id

    @apiParam {String} field target type 'uid', 'pid', 'cid'.
    @apiParam {Number} id target ID.

    @apiSuccess {Json} The graph in json format.
    """
    def __init__(self, **kwargs):
        self.gid_stack = kwargs['gid_stack']

    def get(self, field, value):
        public_gid = int(time.time()) + uuid.uuid4().urn[19:]
        print(public_gid)
        private_gid = uuid.uuid4().urn[9:]
        creator = CreateTlp()
        params = [(field, value)]
        creator.createWithParams(params, private_gid)
        checkTlpFiles(self.gid_stack)
        self.gid_stack.update({public_gid: private_gid})
        return makeResponse({'gid': public_gid})


class CreateGraphWithout(Resource):
    """
    @api {get} /createGraphWithout?type=:type Create a Graph
    @apiName CreateGraphWithout
    @apiGroup Tulip
    @apiDescription Create a graph without given types

    @apiParam {String} type arrays of forbidden type

    @apiSuccess {Json} The graph in json format.
    """
    def __init__(self, **kwargs):
        self.gid_stack = kwargs['gid_stack']

    def get(self):
        public_gid = int(time.time())
        private_gid = uuid.uuid4().urn[9:]
        creator = CreateTlp()
        parser.add_argument('type', action='append')
        args = parser.parse_args()
        creator.createWithout(args['type'], private_gid)
        checkTlpFiles(self.gid_stack)
        self.gid_stack.update({public_gid: private_gid})
        return makeResponse({'gid': public_gid})


class CreateGraphWithParams(Resource):
    """
    @api {get} /createGraph?uid=:uid&pid=:pid&cid=:cid Create a Graph with params
    @apiName CreateGraphWithout
    @apiGroup Tulip
    @apiDescription Create a graph with params

    @apiParam {Number} [uid] arrays of user id
    @apiParam {Number} [pid] arrays of post id
    @apiParam {Number} [cid] arrays of comment id

    @apiSuccess {Json} The graph in json format.
    """
    def __init__(self, **kwargs):
        self.gid_stack = kwargs['gid_stack']

    def get(self):
        public_gid = int(time.time())
        private_gid = uuid.uuid4().urn[9:]
        creator = CreateTlp()
        parser.add_argument('uid', action='append')
        parser.add_argument('pid', action='append')
        parser.add_argument('cid', action='append')
        args = parser.parse_args()
        params = []
        if args['uid']:
            for user in args['uid']:
                params.append(('uid', user))
        if args['pid']:
            for post in args['pid']:
                params.append(('pid', post))
        if args['cid']:
            for comment in args['cid']:
                params.append(('cid', comment))
        creator.createWithParams(params, private_gid)
        checkTlpFiles(self.gid_stack)
        self.gid_stack.update({public_gid: private_gid})
        return makeResponse({'gid': public_gid})


def checkTlpFiles(gid_stack):
    if len(gid_stack) > int(config['api']['max_tlp_files']) - 1:
        keys = gid_stack.copy()
        keys.pop('complete')
        keys.pop('usersToUsers')
        keys.pop('commentAndPost')
        min = 9999999999
        min_key = None
        for key in keys:
            if int(key[0:10]) < min:
                min_key = key
                min = int(key[0:10])
        priv = gid_stack.pop(min_key)
        os.remove('%s%s.tlp' % (config['exporter']['tlp_path'], priv))