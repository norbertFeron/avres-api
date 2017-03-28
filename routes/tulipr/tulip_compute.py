import uuid
import time
import configparser
import os

from flask_restful import Resource, reqparse, request
from routes.utils import makeResponse
from graphtulip.degreeOfInterest import ComputeDoi


config = configparser.ConfigParser()
config.read("config.ini")

parser = reqparse.RequestParser()


class ComputeDOI(Resource):
    def __init__(self, **kwargs):
        self.gid_stack = kwargs['gid_stack']

    def get(self, size):
        selection = request.args.to_dict()
        public_gid = repr(int(time.time())) + uuid.uuid4().urn[19:]
        private_gid = uuid.uuid4().urn[9:]
        computer = ComputeDoi()
        computer.create(private_gid, selection, size)
        checkTlpFiles(self.gid_stack)
        self.gid_stack.update({public_gid: private_gid})
        return makeResponse({'gid': public_gid})


def checkTlpFiles(gid_stack):
    if len(gid_stack) > int(config['api']['max_tlp_files']) - 1:
        keys = gid_stack.copy()
        keys.pop('complete')
        min = 9999999999
        min_key = None
        for key in keys:
            if int(key[0:10]) < min:
                min_key = key
                min = int(key[0:10])
        priv = gid_stack.pop(min_key)
        os.remove('%s%s.tlpb' % (config['exporter']['tlp_path'], priv))