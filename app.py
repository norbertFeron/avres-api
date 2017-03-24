import configparser
import os

from flask import Flask
from flask_restful import Api
from flask_socketio import SocketIO

from routes.tulipr.tulip_routes import add_tulip_routes
from routes.settings.settings_routes import add_settings_routes
from routes.socket.socket_on import add_sockets

config = configparser.ConfigParser()
config.read("config.ini")

if not os.path.exists(config['exporter']['tlp_path']):
    os.makedirs(config['exporter']['tlp_path'])

app = Flask(__name__)
app.config['SECRET_KEY'] = config['socket']['secret_key']

api = Api(app)
socket = SocketIO(app)

add_tulip_routes(api)
add_settings_routes(api)
add_sockets(socket)

if __name__ == '__main__':
    socket.run(app, host=config['api']['host'],
               port=int(config['api']['port']),
               debug=config['api']['debug'])
