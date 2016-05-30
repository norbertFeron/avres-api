from routes.tulip.tulip_doi import ComputeDOI


def add_tulip_routes(api):
    api.add_resource(ComputeDOI, '/doi/<String:interest>')
