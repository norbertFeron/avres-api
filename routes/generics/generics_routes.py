from routes.generics.getters import *
from routes.generics.setters import *
from routes.generics.counters import *


def add_generics_routes(api):

    # GET
    api.add_resource(GetLabels, '/getLabels/')
    api.add_resource(GetLabelsHierarchy, '/getLabelsHierarchy/')
    api.add_resource(GetLabelsByLabel, '/getLabels/<string:label>')
    api.add_resource(GetLabelsById, '/getLabels/<int:id>')

    api.add_resource(GetPropertiesByLabel, '/getProperties/<string:label>')
    api.add_resource(GetPropertyValue, '/getPropertyValue/<string:key>')
    api.add_resource(GetPropertyValueByLabel, '/getPropertyValue/<string:label>/<string:key>')

    api.add_resource(GetAttributesByLabel, '/getAttributes/<string:label>')

    # GET Element(s)
    api.add_resource(GetByLabel, '/get/<string:label>')
    api.add_resource(GetById, '/get/<int:id>')

    # SET
    api.add_resource(SetById, '/set/<int:id>')
    api.add_resource(CreateNew, '/create/')
    api.add_resource(DeleteById, '/<int:id>')

    # COUNT
    api.add_resource(CountLabels, '/countLabels/')
    api.add_resource(CountLabel, '/countLabel/<string:label>')