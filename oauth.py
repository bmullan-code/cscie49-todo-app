from flask import redirect,abort
import os
import pathlib
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from app import session

# extract secret value
# kubectl get secret/oauth-config -o jsonpath={".data.client_secret\.json"}

GOOGLE_CLIENT_ID = url = os.environ.get("GOOGLE_CLIENT_ID")

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

# client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
client_secrets_file = os.path.join("/var/client-secret", "client_secret.json")
print(client_secrets_file)

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid","email"],
    redirect_uri="https://todo.barrymullan.app/callback"
    # redirect_uri="http://localhost:8000/callback"
)

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            # return redirect("/")
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


