
FROM nginx:stable-alpine
COPY default.conf /etc/nginx/conf.d/default.conf

# TODO: make this secure and persistent
RUN mkdir /cache && chmod 777 /cache

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
