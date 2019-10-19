FROM node:11.10.0-alpine as frontend_builder

# npm

WORKDIR /code

RUN npm install yarn -g

ADD front/package.json .
ADD front/yarn.lock .

RUN yarn install --ignore-engines

ADD build build
ADD src src

RUN ls -la
RUN yarn build

FROM nginx:alpine

COPY --from=frontend_builder /code/public/ /usr/share/nginx/html
COPY etc/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80 80
