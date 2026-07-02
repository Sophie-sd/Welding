FROM nginx:1.27-alpine

ARG NGINX_CONF=docker.conf

RUN rm -f /etc/nginx/conf.d/default.conf
COPY deploy/nginx/${NGINX_CONF} /etc/nginx/conf.d/default.conf
