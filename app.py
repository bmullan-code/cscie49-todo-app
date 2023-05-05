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

app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_APP_SECRET_KEY")

@app.route("/login")
def login():
    # authorization_url, state = flow.authorization_url()
    authorization_url, state = flow.authorization_url(access_type='offline',include_granted_scopes='true')
    session["state"] = state
    return redirect(authorization_url)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/")
def index():
    return "Hello World <a href='/login'><button>Login</button></a>"

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")
    return redirect("/todo")

@app.route('/todo')
@login_is_required
def index():
    email = session["email"]
    data = db_fetchall(email)  
    return render_template('index.html', data=data)
 
@app.route('/create', methods=['POST'])
def create():
    # Get the data from the form
    name = request.form['name']
    complete = 1 if request.form.get('complete') else 0
    email = session["email"]

    db_create(email,name,complete)
    # return redirect(url_for('index'))
    return redirect("/todo")
  
@app.route('/update', methods=['POST'])
def update():
    # Get the data from the form
    name = request.form['name']
    complete = 1 if request.form.get('complete') else 0
    id = request.form['id']
    db_update(id,name,complete)
    return redirect("/todo")
    
@app.route('/delete', methods=['POST'])
def delete():
    # Get the data from the form
    id = request.form['id']
    db_delete(id)
    return redirect("/todo")
  
if __name__ == '__main__':
    app.run(debug=True)