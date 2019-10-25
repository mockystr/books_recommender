FROM nginx:1.13-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY --from=docker_recommender-client /code/build/ /usr/share/nginx/html
COPY --from=docker_recommender-client /code/index.html /usr/share/nginx/html
COPY etc/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80 80