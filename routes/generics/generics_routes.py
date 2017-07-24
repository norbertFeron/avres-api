from routes.generics.getters import *


def add_generics_routes(api):

    # GET
    api.add_resource(GetLabels, '/getLabels/<string:label>')
    api.add_resource(GetPropertiesByLabel, '/getProperties/<string:label>')
    api.add_resource(GetPropertyValueByLabel, '/getPropertyValue/<string:label>/<string:key>')

    api.add_resource(GetByLabel, '/get/<string:label>')
    api.add_resource(GetById, '/get/<int:id>')
    api.add_resource(GetByLabelAndId, '/get/<string:label>/<int:id>')
