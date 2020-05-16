FROM alpine:3.11

RUN apk add "dbus" --no-cache

RUN mkdir -p "/broker"
COPY ["broker.conf", "/broker/broker.conf"]

ENTRYPOINT ["dbus-daemon"]
CMD ["--config-file=/broker/broker.conf", "--nofork", "--nosyslog"]