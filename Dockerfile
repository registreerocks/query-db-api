# This API is used to store query information within a mongodb. 
# An nginx server is used as a reverse proxy for the the Swagger/Flask
# API managed using Gunicorn, via Supervisord.

FROM python:3.6

RUN mkdir -p /usr/src
WORKDIR /usr/src

RUN  apt-get update -y && \
     apt-get upgrade -y

# API
RUN mkdir -p /usr/src/package
COPY ./package /usr/src/package
WORKDIR /usr/src/package
RUN pip install -e .

# Deployment
RUN apt-get install supervisor -y
RUN pip install gunicorn


# Supervisord
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Start processes
CMD ["/usr/bin/supervisord"]