from flask import redirect,abort
import os
import pathlib
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from app import session

# Barry Mullan May 2023
# A simple ToDo app that demonstrate an oauth login flow (google) and postgres database persistence

# The oauth module sets up and implements the oauth flow functions
# An oauth client application authenticates with the oauth provider (in this case google) using a 
# previously created client id and client credentials. 

# The client id is stored in a kubernetes secret and injected at runtime as an environment variable
# see the kubernetes/todo-app-deployment.yaml for the details on how this is configured.

# The client credentials is a json file and also stored as a secret, but is mounted as a file under
# the directory /var/client_secret. This configuration is also specified in kubernetes/todo-app-deployment.yaml

# to extract secret value from kubectl cli
# kubectl get secret/oauth-config -o jsonpath={".data.client_secret\.json"}

# set oauth configuration (for dev)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

# retrieve the client id from environement variable
GOOGLE_CLIENT_ID = url = os.environ.get("GOOGLE_CLIENT_ID")

# client_secrets_file is read from mounted volume 
client_secrets_file = os.path.join("/var/client-secret", "client_secret.json")
print(client_secrets_file)

# initialize the flow
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid","email"],
    redirect_uri="https://todo.barrymullan.app/callback"
)




