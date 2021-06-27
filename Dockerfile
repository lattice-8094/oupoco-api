FROM python:3.7

#LABEL maintainer=clement.plancq@ens.fr

RUN mkdir /code
RUN mkdir /code/rss
WORKDIR /code


COPY requirements_rss.txt /code/requirements.txt
RUN pip install -r requirements.txt

COPY generate_rss.py /code/generate_rss.py
COPY generate_serve_rss.sh /code/generate_serve_rss.sh
ENTRYPOINT ["./generate_serve_rss.sh"]
