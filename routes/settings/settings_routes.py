from routes.settings.settings_info import Info


def add_settings_routes(api):

    # Settings
    api.add_resource(Info, '/info')
