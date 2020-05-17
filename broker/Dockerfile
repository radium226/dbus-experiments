FROM docker:19.03

RUN apk add "docker-compose" --no-cache
RUN apk add "dbus" --no-cache
RUN apk add --no-cache syslog-ng

COPY ["./syslog-ng/", "/"]
COPY ["./dbus/", "/broker/dbus"]

ENTRYPOINT []
CMD ["dbus-daemon", "--config-file=/broker/dbus/broker.conf", "--nofork", "--nosyslog"]