import os, sys, inspect

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
print(cmd_folder)
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
# 
# import hug
# # import gevent
#
# from ortelius import api
# import settings
#
# try:
#     env = os.environ['APP_SETTINGS']
# except:
#     env = os.environ['APP_SETTINGS'] = 'development'
#
# if env == 'development':
#     config = settings.DevelopmentConfig
#
# @hug.cli()
# @hug.get('/')
# def welcome():
#     return 'Welcome to ortelius version {0}'.format(config.API_VERSION)
#
#
# @hug.extend_api('/api')
# def get_api():
#     return [api]
#
# if __name__ == '__main__':
#     welcome.interface.cli()
