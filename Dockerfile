FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=sell_tax_free.app

COPY requirements.txt .
RUN pip install --no-cache-dir "flask>=3.0.0,<4" "python-dateutil>=2.8.0" "gunicorn>=22.0.0"

COPY sell_tax_free ./sell_tax_free
COPY templates ./templates
COPY static ./static

ENV PORT=8080
EXPOSE 8080

# Coolify and other hosts often set PORT; Gunicorn is used instead of Flask dev server.
CMD gunicorn --bind 0.0.0.0:${PORT} --workers 2 sell_tax_free.app:app
