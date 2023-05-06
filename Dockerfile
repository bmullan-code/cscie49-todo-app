FROM python:latest
EXPOSE 8000
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["gunicorn", "--workers", "2","--log-level","info","--bind","0.0.0.0:8000", "app:app"]