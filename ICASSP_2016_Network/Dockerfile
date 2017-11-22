FROM python:3.6

RUN wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.0/dumb-init_1.2.0_amd64 && chmod +x /usr/local/bin/dumb-init

RUN mkdir /code
RUN mkdir /webroot
WORKDIR /code

COPY requirements.txt /code
RUN pip --no-cache-dir install -r requirements.txt

# Copy this to webroot so that it's shared to nginx
COPY mp3_carnatic/ /webroot/data/mp3_carnatic/
COPY data/network_files/*.json /webroot/data/network_files/
COPY api/* /code/
COPY uwsgi.ini /code/
COPY scripts/resources/ /webroot/resources/
COPY scripts/index.html /webroot
