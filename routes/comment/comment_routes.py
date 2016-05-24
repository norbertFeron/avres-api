from routes.comment.comment_getter import *
from routes.comment.comment_aggregations import *


def add_comment_routes(api):
    # Getter
    api.add_resource(GetAllComments, '/comments')
    api.add_resource(GetCommentById, '/comment/id/<int:comment_id>')
    api.add_resource(GetAllCommentsByAuthor, '/comments/author/<int:author_id>')

    # Count
    api.add_resource(CountAllComments, '/comments/count/')
    api.add_resource(CountCommentsByAuthor, '/comments/count/author/<int:author_id>')


