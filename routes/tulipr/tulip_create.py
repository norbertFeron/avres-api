import uuid
from flask_restful import Resource, reqparse
from routes.utils import makeResponse
from graphtulip.createtlp import CreateTlp
from graphtulip.createfulltlp import CreateFullTlp
from graphtulip.createusertlp import CreateUserTlp

parser = reqparse.RequestParser()

# Graph generate once


class GenerateFullGraph(Resource):
    def get(self):
        creator = CreateFullTlp()
        creator.create()
        return makeResponse(True)


class GenerateUserGraph(Resource):
    def get(self):
        creator = CreateUserTlp()
        creator.create()
        return makeResponse(True)


class GenerateGraphWithoutUser(Resource):
    def get(self):
        creator = CreateTlp()
        creator.createWithout(["user"], "commentAndPost")
        return makeResponse(True)


class GenerateGraphs(Resource):
    def get(self):
        # Full graph
        creator = CreateFullTlp()
        creator.create()
        # User Graph
        creator = CreateUserTlp()
        creator.create()
        # Comment And Post Graph
        creator = CreateTlp()
        creator.createWithout(["user"], "commentAndPost")
        return makeResponse(True)


# Create new graph


class CreateGraph(Resource):
    def get(self, field, value):
        graph_id = uuid.uuid4()
        creator = CreateTlp()
        params = [(field, value)]
        creator.createWithParams(params, graph_id)
        return makeResponse({'gid': graph_id.urn[9:]})


class CreateGraphWithout(Resource):
    def get(self):
        graph_id = uuid.uuid4()
        creator = CreateTlp()
        parser.add_argument('type', action='append')
        args = parser.parse_args()
        creator.createWithout(args['type'], graph_id)
        return makeResponse({'gid': graph_id.urn[9:]})


class CreateGraphWithParams(Resource):
    def get(self):
        graph_id = uuid.uuid4()
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
        creator.createWithParams(params, graph_id)
        return makeResponse({'gid': graph_id.urn[9:]})
