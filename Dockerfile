FROM ubuntu

RUN apt-get update && apt-get install -y python python-pip
RUN pip install flask flask-sqlalchemy

ADD app.py /srv/app.py
RUN mkdir /srv/templates
ADD templates/index.html /srv/templates/index.html

ENTRYPOINT cd /srv && /usr/bin/python app.py
