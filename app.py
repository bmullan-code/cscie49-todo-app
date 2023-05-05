from flask import Flask, render_template, request, redirect, url_for,session,abort
import psycopg2
import os
import pathlib
import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from database import *
from oauth import *

# Barry Mullan May 2023
# A simple ToDo app that demonstrate an oauth login flow (google) and postgres database persistence

# initialize flask framework
app = Flask(__name__)

# app secret is used to sign session cookies. Read from an env variable which is injected from
# a kubernetes secret (see todo-app-deployment.yaml)
app.secret_key = os.environ.get("FLASK_APP_SECRET_KEY")

# login route, starts oauth authentication flow
@app.route("/login")
def login():
    # authorization_url, state = flow.authorization_url()
    authorization_url, state = flow.authorization_url(access_type='offline',include_granted_scopes='true')
    session["state"] = state
    return redirect(authorization_url)

# logout route, clears the session and redirects to home page
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# default route, home page with login button
@app.route("/")
def index():
    return "Hello World <a href='/login'><button>Login</button></a>"

# callback, registered with google authentication and is called from google once user has 
# authenticated
@app.route("/callback")
def callback():

    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    # create and cache session with flow credentials
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    # store session variables, user name, email etc.
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")
    return redirect("/todo")

# todo route, main application page rendered from template index.html
@app.route('/todo')
@login_is_required
def index():
    # get user email from session
    email = session["email"]
    # fetch data fro this user
    data = db_fetchall(email)  
    # render html page with data
    return render_template('index.html', data=data)

# create route, called to create a new todo item 
@app.route('/create', methods=['POST'])
@login_is_required
def create():
    # get user email from session
    email = session["email"]
    # Get the data from the form
    name = request.form['name']
    # fetch task completion status and set value to 1 if completed (boolean true)
    complete = 1 if request.form.get('complete') else 0
    db_create(email,name,complete)
    # redirect to main todo page
    return redirect("/todo")
  
# update route, called when an item is updated (submit update button)
@app.route('/update', methods=['POST'])
@login_is_required
def update():
    # Get the data from the form
    name = request.form['name']
    complete = 1 if request.form.get('complete') else 0
    id = request.form['id']
    db_update(id,name,complete)
    return redirect("/todo")
    
# delete route, called when an item is delete (submit delete button)
@app.route('/delete', methods=['POST'])
@login_is_required
def delete():
    # Get the data from the form
    id = request.form['id']
    db_delete(id)
    return redirect("/todo")
  
if __name__ == '__main__':
    app.run(debug=True)