FROM alpine:3.22
RUN apk add --no-cache git ca-certificates stagit
COPY sync.sh /sync.sh
COPY style.css favicon.png logo.png /assets/
CMD ["sh", "/sync.sh"]
