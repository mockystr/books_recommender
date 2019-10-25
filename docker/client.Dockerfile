FROM node:11.10.0-alpine as frontend_builder

# npm

WORKDIR /code

ADD front/package.json .
RUN npm i

ENV NODE_ENV production
ENV USE_LOCALHOST 1
ENV LOCALHOST_ADDRESS "http://localhost:1234"
ENV REMOTE_ADDRESS "http://178.128.196.37:1234"

COPY front/ .
COPY scripts scripts

CMD ["./scripts/wait-for-it.sh", "aioserver:1234"]
RUN npm run prod
