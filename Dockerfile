FROM debian:jessie

# GENERAL DEPENDENCIES

RUN apt-get update && \
    apt-get -y install curl

# JAVA
RUN echo "deb http://ftp.debian.org/debian jessie-backports main" | tee -a /etc/apt/sources.list.d/jessie-backports.list
RUN apt-get update
RUN apt-get -y install openjdk-8-jdk

# Pip
RUN apt-get -y install python-pip

# Memcached
#RUN apt-get update
RUN apt-get -y install memcached
RUN pip install python-memcached
RUN pip install gunicorn

# Redis
#RUN apt-get update
RUN apt-get -y install build-essential
RUN apt-get -y install tcl8.5
RUN curl -sL --retry 3 http://download.redis.io/releases/redis-stable.tar.gz > redis-stable.tar.gz
RUN tar xzf redis-stable.tar.gz && cd redis-stable/ && make && make test && make install && cd utils && ./install_server.sh

# CF_RECOMMENDER
RUN pip install cf_recommender

# Cron
RUN apt-get -y install cron
ADD docker/crontab /app/crontab
RUN crontab /app/crontab


# Project env and files
ENV PROJECT_HOME /Preco
RUN mkdir /Preco







ENTRYPOINT ["/Preco/src/main/script/autostart.sh"]
