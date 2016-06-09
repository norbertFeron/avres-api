from flask_restful import reqparse
from flask import make_response
import json
import sys

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


def makeResponse(result, code=200, file=False):
    if file:
        result = [json.load(open(result, 'r', encoding="utf-8"))]
    result = json.dumps(result)
    response = make_response(result, code)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods','GET')
    response.headers.add('Content-Type', 'application/json')
    return response
