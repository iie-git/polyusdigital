FROM python:3.9.7-slim-buster
RUN mkdir -p /code
COPY requirements.txt /code/
WORKDIR /code


RUN python3 -m pip install -r /code/requirements.txt
