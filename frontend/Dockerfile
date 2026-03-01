FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:stable-alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

RUN apk add --no-cache bash

EXPOSE 80

CMD ["bash", "/wait-for-it.sh", "backend:8000", "-t", "90", "--", "nginx", "-g", "daemon off;"]
