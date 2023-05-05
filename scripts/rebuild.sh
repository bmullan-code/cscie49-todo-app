#!/bin/bash
docker build -t todo-app .
docker build --platform "linux/amd64" -t todo-app:x86 .
docker tag todo-app:x86 barrymullan/todo-app:x86
docker push barrymullan/todo-app:x86
docker stop todo-app
docker rm todo-app
docker run --network pg -it --env DATABASE_URL=postgres://postgres:password@postgres:5432/postgres -p 8000:8000 todo-app