FROM hadolint/hadolint:2.12.0-alpine AS hadolint
FROM docker:28.0.4-cli AS docker
FROM node:22-alpine

# OS packages follow the Alpine security repositories.
# hadolint ignore=DL3018
RUN apk add --no-cache python3 py3-pip shellcheck \
    && python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:/opt/lint/node_modules/.bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1
COPY --from=hadolint /bin/hadolint /usr/local/bin/hadolint
COPY --from=docker /usr/local/bin/docker /usr/local/bin/docker
COPY --from=docker /usr/local/libexec/docker/cli-plugins/docker-compose /usr/local/libexec/docker/cli-plugins/docker-compose
WORKDIR /opt/lint
COPY package.json package-lock.json ./
RUN npm ci --ignore-scripts --no-audit --no-fund
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /workspace
ENTRYPOINT ["python3", "linting/run.py"]
