FROM python:3.6
MAINTAINER Clément Plancq <clement.plancq@ens.fr>
#RUN apt-get -y update && apt-get install -y python3 python3-pip libmysqlclient-dev

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

COPY logging.conf /code/logging.conf
COPY app.py /code/app.py
COPY generation_sonnets.py /code/generation_sonnets.py
COPY bd_meta.json /code/bd_meta.json
COPY bd_rimes.json /code/bd_rimes.json
COPY wsgi.py /code/wsgi.py
COPY docker-entrypoint.sh /code/docker-entrypoint.sh
RUN ["chmod", "+x", "/code/docker-entrypoint.sh"]
ENTRYPOINT ["/code/docker-entrypoint.sh"]