from flask_restful import Resource, reqparse
from routes.utils import addargs, makeResponse

parser = reqparse.RequestParser()


class UploadUsersFile(Resource):
    def post(self):
        # todo
        return makeResponse([True], 200)


class UploadPostsFile(Resource):
    def post(self):
        # todo
        return makeResponse([True], 200)


class UploadCommentsFile(Resource):
    def post(self):
        # todo
        return makeResponse([True], 200)