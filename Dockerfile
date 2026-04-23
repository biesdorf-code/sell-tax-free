FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=sell_tax_free.app

COPY requirements.txt .
RUN pip install --no-cache-dir "flask>=3.0.0,<4" "python-dateutil>=2.8.0"

COPY sell_tax_free ./sell_tax_free
COPY templates ./templates
COPY static ./static

EXPOSE 8080

CMD ["python", "-m", "flask", "--app", "sell_tax_free.app", "run", "--host", "0.0.0.0", "--port", "8080"]
