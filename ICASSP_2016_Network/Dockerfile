FROM python:2.7

RUN mkdir /code
RUN mkdir /webroot
WORKDIR /code

COPY requirements.txt /code
RUN pip --no-cache-dir install -r requirements.txt

# Copy this to webroot so that it's shared to nginx
COPY mp3_carnatic/ /webroot/data/mp3_carnatic/
COPY data/network_files/*.json /webroot/data/network_files/
COPY api/* /code/
COPY scripts/resources/ /webroot/resources/
COPY scripts/index.html /webroot