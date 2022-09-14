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
    # Remove temporary files owned by root from the platformtemplate step
    && rm /tmp/* ||true
RUN pip install cryptography==2.8 poetry

COPY ./pyproject.toml /pyproject.toml

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi
COPY . .
# for local development there should be volume to not rebuild image for every change in code, rebuild only when dependencies has changed
EXPOSE 6023