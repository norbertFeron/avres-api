from flask import request
from flask_socketio import emit, join_room, leave_room, \
    close_room, rooms, disconnect

from graphtulip.historyTree import create_trace, load_trace, add_step
from routes.utils import getJson

traces = {}

def add_sockets(socketio):

    @socketio.on('get_trace')
    def get_trace():
        emit('response', {'graph': getJson(load_trace(0))}, json=True)

    @socketio.on('action')
    def action(message):
        new_step = add_step(traces[message['userId']], message['actual'], message['new'])
        emit('response', {'graph': getJson(traces[message['userId']]), 'newStep': new_step}, json=True)

    @socketio.on('join')
    def join(message):
        join_room(message['room'])
        traces[message['userId']] = create_trace(message['initial_step'])
        emit('response', {'log': 'In rooms: ' + ', '.join(rooms()), 'graph': getJson(traces[message['userId']]), "newStep": 0})

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
