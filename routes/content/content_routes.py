from routes.content.content_getter import *
from routes.content.content_aggregations import *


def add_content_routes(api):
    # Getters
    # Multiple
    api.add_resource(GetContents, '/contents')
    api.add_resource(GetContentsByType, '/contents/type/<string:content_type>')
    api.add_resource(GetContentsByAuthor, '/contents/author/<int:author_id>')
    # Single
    api.add_resource(GetContent, '/content/<int:content_id>')
    # Distinct
    api.add_resource(GetContentType, '/content/getType/')

    # Count
    api.add_resource(CountAllContent, '/contents/count/')
    api.add_resource(CountContentByAuthor, '/contents/count/author/<int:author_id>')

    # todo GetContentsByDate(min, max) need to have a fix time format


