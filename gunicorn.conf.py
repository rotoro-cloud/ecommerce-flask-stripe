import os
from dotenv import load_dotenv

bind = '0.0.0.0:5005'
workers = 2
accesslog = '-'
loglevel = 'debug'
capture_output = True
enable_stdio_inheritance = True

for env_file in ('.env', '.flaskenv'):
    env = os.path.join(os.getcwd(), env_file)
    if os.path.exists(env):
        load_dotenv(env)
