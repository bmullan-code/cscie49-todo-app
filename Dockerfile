FROM python:3.10
EXPOSE 8000
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["gunicorn", "--workers", "2","--log-level","debug","--bind","0.0.0.0:8000", "app:app"]