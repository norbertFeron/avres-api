import configparser
import os

from flask import Flask
from flask_restful import Api

from routes.tulipr.tulip_routes import add_tulip_routes
from routes.settings.settings_routes import add_settings_routes

config = configparser.ConfigParser()
config.read("config.ini")

if not os.path.exists(config['exporter']['tlp_path']):
    os.makedirs(config['exporter']['tlp_path'])

app = Flask(__name__)
api = Api(app)

add_tulip_routes(api)
add_settings_routes(api)

if __name__ == '__main__':
    app.run(host=config['api']['host'],
            port=int(config['api']['port']),
            debug=config['api']['debug'],
            threaded = True
            )