from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('limit')


def arglimit():
    args = parser.parse_args()
    if args['limit']:
        return " LIMIT %s" % args['limit']
    else:
        return ''
