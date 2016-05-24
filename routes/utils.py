from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('limit')
parser.add_argument('orderBy')


def addlimit():
    args = parser.parse_args()
    if args['limit']:
        return " LIMIT %s" % args['limit']
    else:
        return ''


def addorderby():
    args = parser.parse_args()
    if args['orderBy']:
        orderby = args['orderBy'].split(':')
        if len(orderby) > 1:
            return " ORDER BY find.%s %s" % (orderby[0], orderby[1])
        else:
            return " ORDER BY find.%s" % orderby[0]
    else:
        return ''


def addargs():
    req = addorderby()
    req += addlimit()
    return req
