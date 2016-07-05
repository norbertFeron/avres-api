import configparser
import os
from flask import Flask
from flask_restful import Api
from routes.user.user_routes import add_user_routes
from routes.comment.comment_routes import add_comment_routes
from routes.post.post_routes import add_post_routes
from routes.tulipr.tulip_routes import add_tulip_routes
from routes.settings.settings_routes import add_settings_routes

from graphtulip.createfulltlp import CreateFullTlp
from graphtulip.createusertlp import CreateUserTlp
from graphtulip.createtlp import CreateTlp


config = configparser.ConfigParser()
config.read("config.ini")

if not os.path.exists(config['exporter']['tlp_path']):
    os.makedirs(config['exporter']['tlp_path'])

app = Flask(__name__)
api = Api(app)

add_user_routes(api)
add_post_routes(api)
add_comment_routes(api)
add_tulip_routes(api)
add_settings_routes(api)

# Todo uncomment for final version
# # Create complete graph
# creatorFull = CreateFullTlp()
# creatorFull.create()
# # Create user graph
# creatorUser = CreateUserTlp()
# creatorUser.create()
# # Create commentAndPost graph
# creator = CreateTlp()
# creator.createWithout(["user"], "commentAndPost")

if __name__ == '__main__':
    app.run(host=config['api']['host'],
            port=int(config['api']['port']),
            debug=config['api']['debug'],
            threaded = True
            )