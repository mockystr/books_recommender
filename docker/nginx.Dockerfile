FROM nginx:1.13-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY etc/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80 80