FROM alpine:3.22
# Follow Alpine's security updates for these system packages.
# hadolint ignore=DL3018
RUN apk add --no-cache git ca-certificates stagit
COPY sync.sh /sync.sh
COPY style.css favicon.png logo.png /assets/
CMD ["sh", "/sync.sh"]
