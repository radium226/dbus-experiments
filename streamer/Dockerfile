FROM python:3.8-alpine3.11

ENV POETRY_VERSION 1.0.5

RUN apk add "gcc" --no-cache
RUN apk add "python3-dev" --no-cache
RUN apk add "musl-dev" --no-cache
RUN apk add "libffi-dev" --no-cache
RUN apk add "openssl-dev" --no-cache
RUN pip install "poetry==${POETRY_VERSION}"

# dbus-python packages
RUN apk add "dbus" "dbus-dev" "glib-dev" "autoconf-archive" "py3-sphinx" --no-cache # --virtual ".build-deps"

# pygobject packages
RUN apk add "cairo-dev" "pkgconfig" "gobject-introspection-dev" --no-cache # --virtual ".build-deps"

# ffmpeg
RUN apk add "ffmpeg"

ARG UID
ARG GID
RUN addgroup --gid="${GID}" "streamer"
RUN adduser --home "/streamer" --uid "${UID}" --ingroup "streamer" --disabled-password "streamer"
WORKDIR "/streamer"
USER "streamer"

RUN poetry config virtualenvs.create false --no-interaction --no-ansi
COPY ["./pyproject.toml", "."]
COPY ["./poetry.lock", "."]
RUN poetry install --no-interaction --no-ansi

# Remove packages
# RUN apk del ".build-deps"

COPY [".", "."]
ENTRYPOINT ["poetry", "run", "streamer"]
CMD []