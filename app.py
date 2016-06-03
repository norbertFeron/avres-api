import configparser
from flask import Flask
from flask_restful import Api
from routes.user.user_routes import add_user_routes
from routes.comment.comment_routes import add_comment_routes
from routes.post.post_routes import add_post_routes
from routes.tulipr.tulip_routes import add_tulip_routes
from update_database import Update, HardUpdate, CreateTlp

config = configparser.ConfigParser()
config.read("config.ini")

app = Flask(__name__)
api = Api(app)

add_user_routes(api)
add_post_routes(api)
add_comment_routes(api)
add_tulip_routes(api)

# todo remove temporary route
api.add_resource(Update, '/update')
api.add_resource(HardUpdate, '/hardUpdate')
api.add_resource(CreateTlp, '/createtlp')

# todo load the complete graph to a tlp instance for big compute like DOI


if __name__ == '__main__':
    app.run(host=config['api']['host'],
            port=int(config['api']['port']),
            debug=config['api']['debug']
            )