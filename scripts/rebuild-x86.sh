#!/bin/bash
docker build --platform "linux/amd64" -t todo-app-x86 .
docker tag todo-app-x86 barrymullan/todo-app-x86
docker push barrymullan/todo-app-x86
