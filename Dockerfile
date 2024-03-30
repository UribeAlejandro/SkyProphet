# pull official base image
FROM python:3.12.1-slim-bookworm

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY requirements.txt requirements.txt

# install python dependencies
RUN pip install -r requirements.txt

# add app
COPY . .

# run gunicorn
CMD gunicorn --bind 0.0.0.0:$PORT challenge.api:app -k uvicorn.workers.UvicornWorker
