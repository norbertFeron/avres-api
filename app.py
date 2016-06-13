import configparser
import os
from flask import Flask
from flask_restful import Api
from routes.user.user_routes import add_user_routes
from routes.comment.comment_routes import add_comment_routes
from routes.post.post_routes import add_post_routes
from routes.tulipr.tulip_routes import add_tulip_routes
from update_database import Update, HardUpdate

config = configparser.ConfigParser()
config.read("config.ini")

if not os.path.exists(config['exporter']['tlp_path']):
    os.makedirs(config['exporter']['tlp_path'])
if not os.path.exists(config['exporter']['json_path']):
    os.makedirs(config['exporter']['json_path'])

app = Flask(__name__)
api = Api(app)

add_user_routes(api)
add_post_routes(api)
add_comment_routes(api)
add_tulip_routes(api)

# todo remove temporary route
api.add_resource(Update, '/update')
api.add_resource(HardUpdate, '/hardUpdate')

# todo load the complete graph to a tlp instance for big compute like DOI


if __name__ == '__main__':
    app.run(host=config['api']['host'],
            port=int(config['api']['port']),
            debug=config['api']['debug'],
            threaded = True
            )