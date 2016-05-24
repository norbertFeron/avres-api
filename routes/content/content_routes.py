from routes.content.content_getter import *
from routes.content.content_aggregations import *


def add_content_routes(api):
    # Getters
    # Multiple
    api.add_resource(GetAllContents, '/contents')
    api.add_resource(GetAllContentsByType, '/contents/type/<string:content_type>')
    api.add_resource(GetAllContentsByAuthor, '/contents/author/<int:author_id>')
    # Single
    api.add_resource(GetContentById, '/content/id/<int:content_id>')
    # Count
    api.add_resource(CountAllContent, '/contents/count/')
    api.add_resource(CountContentByAuthor, '/contents/count/author/<int:author_id>')

# todo GetAllType
