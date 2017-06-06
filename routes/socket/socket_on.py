from flask import request
from flask_socketio import emit, join_room, leave_room, \
    close_room, rooms, disconnect
from tulip import *

from graphtulip.manage import onJoin, load, addStep, getStep, getNodes
from routes.utils import getJson

def add_sockets(socketio):

    @socketio.on('load_trace')
    def load_trace(message):
        trace, step = load(message)
        emit('response', {'type': 'get_trace', 'data': {"graph": getJson(trace), "step": step, 'user': message['user']}}, json=True)

    @socketio.on('get_nodes')
    def get_nodes():
        emit('response', {'type': 'get_nodes', 'data': getNodes()}, json=True)

    @socketio.on('get_layouts')
    def get_layouts():
        emit('response', {'type': 'get_layouts', 'data': tlp.getLayoutAlgorithmPluginsList()}, json=True)

    @socketio.on('get_step')
    def get_step(message):
        graph = getStep(message['step'])
        emit('response', {'type': 'get_step', 'data': {'graph': getJson(graph), 'step': message['step']}}, json=True)

    @socketio.on('action')
    def action(message):
        trace, step = addStep(message)
        emit('response', {'type': 'get_trace', 'data': {"graph": getJson(trace), "step": step,  'user': message['user']}}, json=True, room=message['room'])
        # emit('response', {'type': 'get_step', 'data': {"graph": getJson(doi), "step": step}})

    # @socketio.on('annotate')
    # def annotate(message):
    #     trace, graph = add_annotation(message)
    #     emit('response', {'type': 'get_trace', 'data': {"graph": getJson(trace), "step": message['step'],  'user': message['user']}}, json=True, room=message['room'])
    #     emit('response', {'type': 'get_step', 'data': {"graph": getJson(graph), "step": message['step']}})


    @socketio.on('join')
    def join(message):
        join_room(message['room'])
        trace, step = onJoin(message['type'], message['room'])
        emit('response', {'type': 'join'})
        emit('response', {'type': 'get_trace', 'data': {"graph": getJson(trace), 'step': step, 'user': message['user']}}, json=True)

    @socketio.on('leave')
    def leave(message):
        leave_room(message['room'])
        emit('response', {'type': 'leave'})

    @socketio.on('focus')
    def send_room_focus(message):
        emit('response', {'type': 'focus', 'data': {'user': message['user'], 'step': message['step']}}, room=message['room'])

    @socketio.on('disconnect_request')
    def disconnect_request():
        emit('response',
             {'data': 'Disconnected!'})
        disconnect()

    @socketio.on('disconnect')
    def test_disconnect():
        print('Client disconnected', request.sid)
