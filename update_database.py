from importer.importFromJson import ImportFromJson
from flask_restful import Resource
from graphtulip.createfulltlp import CreateFullTlp
from graphtulip.createtlp import CreateTlp


class Update(Resource):
    def get(self):
        importer = ImportFromJson(False)
        importer.create_users()
        importer.create_posts()
        importer.create_comments()
        return importer.end_import()


class HardUpdate(Resource):
    def get(self):
        importer = ImportFromJson(True)
        importer.create_users()
        importer.create_posts()
        importer.create_comments()
        importer.end_import()
        return importer.end_import()


class GetCreateTlpFull(Resource):
    def get(self):
        creator = CreateFullTlp()
        creator.create()
        return True


class GetCreateTlp(Resource):
    def get(self):
        creator = CreateTlp()
        creator.create("uid", "32", "noemi")
        return True

if __name__ == '__main__':
    importer = ImportFromJson()
    importer.create_users()
    importer.create_posts()
    importer.create_comments()
    importer.end_import()
