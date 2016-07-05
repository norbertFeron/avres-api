import uuid
from flask_restful import Resource, reqparse
from routes.utils import makeResponse
from graphtulip.degreeOfInterest import create

parser = reqparse.RequestParser()


class ComputeDOI(Resource):
    def get(self, graph, type, id):
        parser.add_argument('max_size', type=int)
        args = parser.parse_args()
        graph_id = uuid.uuid4()
        if args['max_size']:
            create(graph, graph_id, type, id, args['max_size'])
        else:
            create(graph, graph_id, type, id)
        return makeResponse({'gid': graph_id.urn[9:]})
