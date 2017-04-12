from flask import request
from flask_socketio import emit, join_room, leave_room, \
    close_room, rooms, disconnect
from tulip import *

from graphtulip.manage import create, load, add_step
from routes.utils import getJson

def add_sockets(socketio):

    @socketio.on('load_trace')
    def load_trace(message):
        trace, step = load(message)
        emit('response', {'type': 'get_trace', 'data': {"graph": getJson(trace), "step": step}}, json=True)

    @socketio.on('get_layouts')
    def get_layouts():
        emit('response', {'type': 'get_layouts', 'data': tlp.getLayoutAlgorithmPluginsList()}, json=True)

    @socketio.on('action')
    def action(message):
        trace, doi, step = add_step(message)
        emit('response', {'type': 'get_trace', 'data': {"graph": getJson(trace), "step": step}}, json=True)
        emit('response', {'type': 'get_step', 'data': {"graph": getJson(doi), "step": step}})

    @socketio.on('join')
    def join(message):
        join_room(message['room'])
        trace = create(message['type'], message['userId'])
        emit('response', {'log': 'In rooms: ' + ', '.join(rooms())})

    @socketio.on('leave')
    def leave(message):
        leave_room(message['room'])
        emit('response', {'data': 'In rooms: ' + ', '.join(rooms())})

    @socketio.on('close_room')
    def close(message):
        emit('response', {'data': 'Room ' + message['room'] + ' is closing.'}, room=message['room'])
        close_room(message['room'])

    @socketio.on('my_room_event')
    def send_room_message(message):
        emit('response',
             {'data': message['data']}, room=message['room'])

    @socketio.on('disconnect_request')
    def disconnect_request():
        emit('response',
             {'data': 'Disconnected!'})
        disconnect()

    @socketio.on('disconnect')
    def test_disconnect():
        print('Client disconnected', request.sid)
