FROM ubuntu:xenial

RUN apt-get update && apt-get install -y python3 python3-yaml python3-flask graphviz

RUN mkdir /heat2d3

ADD *py /heat2d3/

ADD static /heat2d3/static

ADD template.html /heat2d3/

ADD docker-entrypoint.sh /

CMD /docker-entrypoint.sh

EXPOSE 1112
