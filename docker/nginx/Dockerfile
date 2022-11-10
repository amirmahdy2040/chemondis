FROM nginx:1.22.0-alpine

RUN mkdir /src
RUN rm /etc/nginx/conf.d/default.conf
COPY ./docker/nginx/nginx.conf /etc/nginx/conf.d/
WORKDIR /src