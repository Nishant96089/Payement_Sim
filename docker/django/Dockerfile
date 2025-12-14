FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean

COPY backend/requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

CMD ["sh", "-c", "python backend/manage.py runserver 0.0.0.0:8000"]
