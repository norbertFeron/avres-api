import configparser
import os

from flask import Flask
from flask_socketio import SocketIO

from routes.socket.socket_on import add_sockets

config = configparser.ConfigParser()
config.read("config.ini")

if not os.path.exists(config['exporter']['tlp_path']):
    os.makedirs(config['exporter']['tlp_path'])

app = Flask(__name__)
app.config['SECRET_KEY'] = config['socket']['secret_key']

socket = SocketIO(app)

add_sockets(socket)

if __name__ == '__main__':
    socket.run(app, host=config['socket']['host'],
               port=int(config['socket']['port']),
               debug=config['socket']['debug'])
