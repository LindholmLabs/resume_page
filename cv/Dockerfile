FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && useradd --uid 10001 --create-home resume \
    && chown resume:resume /app

COPY --chown=resume:resume main.py index.html style.css favicon.svg robots.txt sitemap.xml ./
USER resume
EXPOSE 8000
CMD ["python", "main.py"]
