FROM python:3.10-slim
WORKDIR /app
RUN pip install fastapi uvicorn prometheus-client celery
COPY app.py tasks.py ./
EXPOSE 8000