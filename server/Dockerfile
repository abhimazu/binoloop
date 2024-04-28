FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV MODEL_NAME=microsoft/phi-2

ENV NUM_WORKERS=1

CMD uvicorn server:app --host 0.0.0.0 --port 8000 --workers $NUM_WORKERS
