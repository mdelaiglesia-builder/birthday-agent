FROM python:3.12-slim

WORKDIR /app

COPY phase5-production/requirements.txt phase5-production/requirements.txt
RUN pip install --no-cache-dir -r phase5-production/requirements.txt

COPY phase3-rag/ phase3-rag/
COPY phase4-agent/ phase4-agent/
COPY phase5-production/ phase5-production/

WORKDIR /app/phase5-production

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]