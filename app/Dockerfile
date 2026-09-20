FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
RUN pip install --no-cache-dir Flask==3.1.2 waitress==3.0.2 \
    && useradd --uid 10001 --create-home resume \
    && chown resume:resume /app

COPY --chown=resume:resume main.py index.html style.css ./
USER resume
EXPOSE 8000
CMD ["python", "main.py"]
