from flask import request
from flask_socketio import emit, join_room, leave_room, \
    close_room, rooms, disconnect
from tulip import *

from graphtulip.manage import create, load, addStep, getStep
from routes.utils import getJson

def add_sockets(socketio):

    @socketio.on('load_trace')
    def load_trace(message):
        trace, step = load(message)
        emit('response', {'type': 'get_trace', 'data': {"graph": getJson(trace), "step": step}}, json=True)

    @socketio.on('get_layouts')
    def get_layouts():
        emit('response', {'type': 'get_layouts', 'data': tlp.getLayoutAlgorithmPluginsList()}, json=True)

    @socketio.on('get_step')
    def get_step(message):
        graph = getStep(message['room'], message['step'])
        emit('response', {'type': 'reload_step', 'data': {'graph': getJson(graph), 'step': message['step']}}, json=True)

    @socketio.on('action')
    def action(message):
        trace, doi, step = addStep(message)
        emit('response', {'type': 'get_trace', 'data': {"graph": getJson(trace), "step": step}}, json=True, room=message['room'])
        emit('response', {'type': 'get_step', 'data': {"graph": getJson(doi), "step": step}}, room=message['room'])

    @socketio.on('join')
    def join(message):
        join_room(message['room'])
        trace = create(message['type'], message['room'])
        emit('response', {'type': 'join'})
        emit('response', {'type': 'get_trace', 'data': {"graph": getJson(trace)}}, json=True)


    @socketio.on('leave')
    def leave(message):
        leave_room(message['room'])
        emit('response', {'type': 'leave'})

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
