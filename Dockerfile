FROM python:3.8

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get clean && apt-get update && \
    apt-get -y install --no-install-recommends \
    gcc \
    libev-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install pip bjoern --upgrade

COPY ./scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./scripts/run.sh /run.sh
COPY ./scripts/run.py /run.py
RUN chmod +x /run.sh

COPY ./app /app
WORKDIR /app/

ENV PYTHONPATH=/app

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/run.sh"]