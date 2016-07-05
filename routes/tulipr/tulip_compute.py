import uuid
from flask_restful import Resource, reqparse
from routes.utils import makeResponse
from graphtulip.degreeOfInterest import create

parser = reqparse.RequestParser()


class ComputeDOI(Resource):
    def __init__(self, **kwargs):
        self.gid_stack = kwargs['gid_stack']

    def get(self, graph, type, id):
        private_source = self.gid_stack[graph]
        parser.add_argument('max_size', type=int)
        args = parser.parse_args()
        public_gid = uuid.uuid4().urn[9:]
        private_gid = uuid.uuid4().urn[9:]
        if args['max_size']:
            create(private_source, private_gid, type, id, args['max_size'])
        else:
            create(private_source, private_gid, type, id)
        self.gid_stack.update({public_gid: private_gid})
        return makeResponse({'gid': public_gid})
