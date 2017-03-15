import uuid
import time
from flask_restful import Resource, reqparse, request
from routes.utils import makeResponse
from graphtulip.degreeOfInterest import create
from routes.tulipr.tulip_create import checkTlpFiles

parser = reqparse.RequestParser()


class ComputeDOI(Resource):
    def __init__(self, **kwargs):
        self.gid_stack = kwargs['gid_stack']

    def get(self):
        selection = request.args.to_dict()
        public_gid = repr(int(time.time())) + uuid.uuid4().urn[19:]
        private_gid = uuid.uuid4().urn[9:]
        create(private_gid, selection)
        checkTlpFiles(self.gid_stack)
        self.gid_stack.update({public_gid: private_gid})
        return makeResponse({'gid': public_gid})
