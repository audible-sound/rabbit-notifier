FROM python:3.14-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --upgrade pip \ 
    && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"] # Will be overriden by commands in docker compose
