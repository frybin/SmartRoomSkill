import secrets
from os import environ as env

# Flask config
IP = env.get('IP', '0.0.0.0')
PORT = env.get('PORT', 8080)
SERVER_NAME = env.get('SERVER_NAME', 'alexa-smart-endpoint-alexaroom.a.csh.rit.edu')

# Openshift secret
SECRET_KEY = env.get("SECRET_KEY", default=''.join(secrets.token_hex(16)))
