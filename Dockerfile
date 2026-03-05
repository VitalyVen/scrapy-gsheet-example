FROM python:3.10-slim-buster
ENV LANG=C LC_ALL=C PYTHONUNBUFFERED=1
RUN \
    DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl git \
    && apt-get clean autoclean \
    && apt-get autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* \
    && rm -f /var/cache/apt/archives/*.deb \
    && rm -f /tmp/* ||true

RUN pip install --no-cache-dir uv

COPY ./pyproject.toml ./uv.lock /

RUN uv sync --frozen

COPY . .

EXPOSE 6023
