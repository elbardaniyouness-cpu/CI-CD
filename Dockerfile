FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY service/ ./service/

# OpenShift runs containers as a random non-root UID
RUN useradd --uid 1000 counter && chown -R counter /app
USER 1000

ENV PORT=8000
EXPOSE $PORT
CMD ["gunicorn", "--bind=0.0.0.0:8000", "--log-level=info", "service:app"]
