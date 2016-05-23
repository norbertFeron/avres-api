import configparser
from flask import Flask
from flask_restful import Api
from routes.user.user_route import *
from routes.comment.comment_route import *
from routes.content.content_route import *

config = configparser.ConfigParser()
config.read("config.ini")

app = Flask(__name__)
api = Api(app)

#### USERS Routes ####
api.add_resource(GetAllUsers, '/users')
# ...
api.add_resource(GetUserById, '/user/id/<int:user_id>')
api.add_resource(GetUserByName, '/user/name/<string:user_name>')
# ...

#### COMMENTS Routes ####
api.add_resource(GetAllComments, '/comments')
# ...
api.add_resource(GetCommentById, '/comment/id/<int:comment_id>')
api.add_resource(GetCommentByTitle, '/comment/title/<string:comment_title>')
# ...

#### COMMENTS Routes ####
api.add_resource(GetAllContents, '/contents')
api.add_resource(GetAllContentsByType, '/contents/type/<string:content_type>')
# ...
api.add_resource(GetContentById, '/content/id/<int:content_id>')
api.add_resource(GetContentByTitle, '/content/title/<string:content_title>')
# ...

if __name__ == '__main__':
    app.run(host=config['api']['host'],
            port=int(config['api']['port']),
            debug=config['api']['debug']
            )

# todo requirements.txt