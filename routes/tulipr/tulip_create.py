import uuid
from flask_restful import Resource, reqparse
from routes.utils import makeResponse
from graphtulip.createtlp import CreateTlp
from graphtulip.createfulltlp import CreateFullTlp
from graphtulip.createusertlp import CreateUserTlp
from graphtulip.degreeOfInterest import DOIContext

parser = reqparse.RequestParser()


class CreateFullGraph(Resource):
    def get(self):
        creator = CreateFullTlp()
        creator.create()
        return True


class CreateUserGraph(Resource):
    def get(self):
        creator = CreateUserTlp()
        creator.create()
        return True


class CreateGraph(Resource):
    def get(self, field, value):
        graph_id = uuid.uuid4()
        creator = CreateTlp()
        creator.create(field, value, graph_id)
        return makeResponse([graph_id.urn[9:]])
