FROM python:3.7
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
COPY rhymes_1.json /code/rhymes_1.json
COPY rhymes_2.json /code/rhymes_2.json
COPY rhymes_3.json /code/rhymes_3.json
COPY selected_authors.json /code/selected_authors.json
COPY wsgi.py /code/wsgi.py
COPY docker-entrypoint.sh /code/docker-entrypoint.sh
RUN ["chmod", "+x", "/code/docker-entrypoint.sh"]
ENTRYPOINT ["/code/docker-entrypoint.sh"]