# build env
FROM node:13.12.0-alpine as build
# RUN echo 1
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . ./
RUN npm run build
CMD cp -r build result_build
