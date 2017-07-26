import configparser
import os

from flask import Flask
from flask_restful import Api

from routes.generics.generics_routes import add_generics_routes
from routes.tulipr.tulip_routes import add_tulip_routes
from routes.settings.settings_routes import add_settings_routes

config = configparser.ConfigParser()
config.read("config.ini")

app = Flask(__name__)
api = Api(app)

add_generics_routes(api)
add_tulip_routes(api)
add_settings_routes(api)

if __name__ == '__main__':
    app.run(host=config['api']['host'],
            port=int(config['api']['port']),
            debug=config['api']['debug'],
            threaded = True
            )