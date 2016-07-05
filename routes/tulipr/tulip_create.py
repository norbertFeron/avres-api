import uuid
from flask_restful import Resource, reqparse
from routes.utils import makeResponse
from graphtulip.createtlp import CreateTlp
from graphtulip.createfulltlp import CreateFullTlp
from graphtulip.createusertlp import CreateUserTlp

parser = reqparse.RequestParser()

# Graph generate once


class GenerateFullGraph(Resource):
    def __init__(self, **kwargs):
        self.gid_stack = kwargs['gid_stack']

    def get(self):
        private_gid = uuid.uuid4().urn[9:]
        creator = CreateFullTlp()
        creator.create(private_gid)
        self.gid_stack.update({"complete": private_gid})
        return makeResponse(True)


class GenerateUserGraph(Resource):
    def __init__(self, **kwargs):
        self.gid_stack = kwargs['gid_stack']

    def get(self):
        private_gid = uuid.uuid4().urn[9:]
        creator = CreateUserTlp()
        creator.create(private_gid)
        self.gid_stack.update({"complete": private_gid})
        return makeResponse(True)


class GenerateGraphWithoutUser(Resource):
    def __init__(self, **kwargs):
        self.gid_stack = kwargs['gid_stack']

    def get(self):
        private_gid = uuid.uuid4().urn[9:]
        creator = CreateTlp()
        creator.createWithout(["user"], private_gid)
        self.gid_stack.update({"complete": private_gid})
        return makeResponse(True)


class GenerateGraphs(Resource):
    def __init__(self, **kwargs):
        self.gid_stack = kwargs['gid_stack']

    def get(self):
        # Full graph
        creator = CreateFullTlp()
        complete_gid = uuid.uuid4().urn[9:]
        creator.create(complete_gid)
        self.gid_stack.update({"complete": complete_gid})
        # User Graph
        creator = CreateUserTlp()
        users_gid = uuid.uuid4().urn[9:]
        creator.create(users_gid)
        self.gid_stack.update({"usersToUsers": users_gid})
        # Comment And Post Graph
        creator = CreateTlp()
        commentPost_gid = uuid.uuid4().urn[9:]
        creator.createWithout(["user"], commentPost_gid)
        self.gid_stack.update({"commentAndPost": commentPost_gid})
        return makeResponse(True)


# Create new graph


class CreateGraph(Resource):
    def __init__(self, **kwargs):
        self.gid_stack = kwargs['gid_stack']

    def get(self, field, value):
        public_gid = uuid.uuid4().urn[9:]
        private_gid = uuid.uuid4().urn[9:]
        creator = CreateTlp()
        params = [(field, value)]
        creator.createWithParams(params, private_gid)
        self.gid_stack.update({public_gid: private_gid})
        return makeResponse({'gid': public_gid})


class CreateGraphWithout(Resource):
    def __init__(self, **kwargs):
        self.gid_stack = kwargs['gid_stack']

    def get(self):
        public_gid = uuid.uuid4().urn[9:]
        private_gid = uuid.uuid4().urn[9:]
        creator = CreateTlp()
        parser.add_argument('type', action='append')
        args = parser.parse_args()
        creator.createWithout(args['type'], private_gid)
        self.gid_stack.update({public_gid: private_gid})
        return makeResponse({'gid': public_gid})


class CreateGraphWithParams(Resource):
    def __init__(self, **kwargs):
        self.gid_stack = kwargs['gid_stack']

    def get(self):
        public_gid = uuid.uuid4().urn[9:]
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
        self.gid_stack.update({public_gid: private_gid})
        return makeResponse({'gid': public_gid})
