FROM python:3.8-alpine3.11

ENV POETRY_VERSION 1.0.5

RUN apk add "gcc" --no-cache
RUN apk add "python3-dev" --no-cache
RUN apk add "musl-dev" --no-cache
RUN apk add "libffi-dev" --no-cache
RUN apk add "openssl-dev" --no-cache
RUN pip install "poetry==${POETRY_VERSION}"

# ffmpeg
RUN apk add "ffmpeg"

# zeromq
RUN apk add "zeromq" "zeromq-dev"

ARG UID
ARG GID
RUN addgroup --gid="${GID}" "streaming"
RUN adduser --home "/streaming" --uid "${UID}" --ingroup "streaming" --disabled-password "streaming"
WORKDIR "/streaming"
USER "streaming"

RUN poetry config virtualenvs.create false --no-interaction --no-ansi
COPY ["./pyproject.toml", "."]
COPY ["./poetry.lock", "."]
RUN poetry install --no-interaction --no-ansi

COPY [".", "."]
ENTRYPOINT ["poetry", "run", "streaming"]
CMD []