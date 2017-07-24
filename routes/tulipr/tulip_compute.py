import uuid
import time
from flask_restful import Resource, reqparse
from routes.utils import makeResponse
from graphtulip.degreeOfInterest import create
from routes.tulipr.tulip_create import checkTlpFiles

parser = reqparse.RequestParser()


class ComputeDOI(Resource):
    """
    @api {get} /doi/:graph_id/:type/:id?max_size=:max_size Create doi sub-graph
    @apiName ComputeDOI
    @apiGroup Tulip
    @apiDescription Create a sub graph base on Degree of interest

    @apiParam {Number} graph_id Base public graph id.
    @apiParam {String} type Type of the target 'uid', 'pid' or 'cid'
    @apiParam {Number} id Id of the target
    @apiParam {Number} max_size Max size of the sub-graph

    @apiSuccess {Json} The sub-graph in json format.
    """
    def __init__(self, **kwargs):
        self.gid_stack = kwargs['gid_stack']

    def get(self, graph, type, id):
        private_source = self.gid_stack[graph]
        parser.add_argument('max_size', type=int)
        args = parser.parse_args()
        public_gid = repr(int(time.time())) + uuid.uuid4().urn[19:]
        private_gid = uuid.uuid4().urn[9:]
        if args['max_size']:
            create(private_source, private_gid, type, id, args['max_size'])
        else:
            create(private_source, private_gid, type, id)
        checkTlpFiles(self.gid_stack)
        self.gid_stack.update({public_gid: private_gid})
        return makeResponse({'gid': public_gid})
