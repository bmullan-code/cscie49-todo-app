#!/bin/bash

# create kubernetes secrets from contents of secrets files

# postgres database super user and replica passwords
kubectl delete secret/mypostgres-secret
kubectl create secret generic mypostgres-secret --from-literal=superUserPassword=$(cat postgres_superuser_pw.txt | xargs echo -n) --from-literal=replicationUserPassword=$(cat postgres_replicauser_pw.txt | xargs echo -n)

# oauth google client id
kubectl delete secret/google-client-id-secret
kubectl create secret generic google-client-id-secret --from-literal=GOOGLE_CLIENT_ID=$(cat google_client_id.txt | xargs echo -n)

# oauth google application credentials file (mounted as a file to the pod, see deployment)
kubectl delete secret/client-secret
kubectl create secret generic client-secret --from-file=client_secret.json

# secret key used by flask app to sign session cookies. Should be consistent accross pods and runs
kubectl delete secret/flask-app-secret-key
kubectl create secret generic flask-app-secret-key --from-literal=FLASK_APP_SECRET_KEY=$(cat flask_app_secret_key.txt | xargs echo -n)

# secret with postgres url for the todo-app
kubectl delete secret/todo-app
kubectl create secret generic todo-app --from-literal=postgres-url=$(cat postgres_url.txt | xargs echo -n)




