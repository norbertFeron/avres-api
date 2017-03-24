from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect


def add_sockets(socketio):

    @socketio.on('message')
    def handle_message(message):
        print('received message: ' + message)

    @socketio.on('join')
    def join(message):
        join_room(message['room'])
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('response',
             {'data': 'In rooms: ' + ', '.join(rooms()),
              'count': session['receive_count']})

    @socketio.on('leave')
    def leave(message):
        leave_room(message['room'])
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('response',
             {'data': 'In rooms: ' + ', '.join(rooms()),
              'count': session['receive_count']})

    @socketio.on('close_room')
    def close(message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('response', {'data': 'Room ' + message['room'] + ' is closing.',
                             'count': session['receive_count']},
             room=message['room'])
        close_room(message['room'])

    @socketio.on('my_room_event')
    def send_room_message(message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('response',
             {'data': message['data'], 'count': session['receive_count']},
             room=message['room'])

    @socketio.on('disconnect_request')
    def disconnect_request():
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('response',
             {'data': 'Disconnected!', 'count': session['receive_count']})
        disconnect()

    @socketio.on('disconnect')
    def test_disconnect():
        print('Client disconnected', request.sid)
