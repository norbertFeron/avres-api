from routes.comment.comment_getter import *
from routes.comment.comment_aggregations import *


def add_comment_routes(api):
    # Getter
    # Multiple
    api.add_resource(GetAllComments, '/comments')
    api.add_resource(GetAllCommentsByAuthor, '/comments/author/<int:author_id>')
    api.add_resource(GetAllCommentsOnContent, '/comments/content/<int:content_id>')
    api.add_resource(GetAllCommentsOnComment, '/comments/comment/<int:comment_id>')
    # Simple
    api.add_resource(GetComment, '/comment/<int:comment_id>')

    # Count
    api.add_resource(CountAllComments, '/comments/count/')
    api.add_resource(CountCommentsByAuthor, '/comments/count/author/<int:author_id>')


