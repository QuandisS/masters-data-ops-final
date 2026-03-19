FROM python:3.14-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        gnupg \
        && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
        && apt-get install -y nodejs \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

RUN npm install -g configurable-http-proxy

RUN pip install --no-cache-dir jupyterhub jupyterhub-dummyauthenticator

RUN useradd -m -s /bin/bash jupyter && \
    mkdir -p /srv/jupyterhub && \
    chown -R jupyter:jupyter /srv/jupyterhub

WORKDIR /srv/jupyterhub

USER jupyter

EXPOSE 8000

CMD ["jupyterhub", "-f", "/etc/jupyterhub/jupyterhub_config.py"]