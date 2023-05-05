#!/bin/bash
docker build -t todo-app .
docker tag todo-app barrymullan/todo-app
docker push barrymullan/todo-app
docker stop todo-app
docker rm todo-app
docker run --network pg -it --mount type=bind,source="$(pwd)"/kubernetes/secrets/client_secret.json,target=/var/client-secret/client_secret.json,readonly --env DATABASE_URL=postgres://postgres:password@postgres:5432/postgres -p 8000:8000 todo-app