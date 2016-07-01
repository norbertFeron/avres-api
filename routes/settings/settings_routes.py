from routes.settings.settings_upload import UploadUsersFile, UploadPostsFile, UploadCommentsFile
from routes.settings.settings_update import Update, HardUpdate, Info


def add_settings_routes(api):
    # Upload
    api.add_resource(UploadUsersFile, '/upload/users')
    api.add_resource(UploadPostsFile, '/upload/posts')
    api.add_resource(UploadCommentsFile, '/upload/comments')

    # Update
    api.add_resource(Info, '/info')
    api.add_resource(HardUpdate, '/hardUpdate')
    api.add_resource(Update, '/update')
