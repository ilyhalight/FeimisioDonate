import os
import logging

from config.load import load_env, load_cfg


load_env()
logs = load_cfg()['LOGGING']
env_port = os.environ.get('PORT')


PORT = int(env_port) if env_port else 5000
accesslog = logging.getLogger('server')
errorlog = logging.getLogger('server')
debug = True
bind = f'0.0.0.0:{PORT}'
use_reloader = True
loglevel = logging.getLevelName(logs['server_lvl'])