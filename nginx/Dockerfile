FROM nginx:1.20.1
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY nginx.dev.conf /tmp
ARG BUILD_TYPE=prod
RUN if ["${BUILD_TYPE}" = "dev"]; then \
    mv /tmp/nginx.dev.conf /etc/nginx/conf.d/default.conf ;\
    fi