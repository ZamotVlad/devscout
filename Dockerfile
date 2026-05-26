# Використовуємо офіційний легкий образ Python
FROM python:3.11-slim

# Встановлюємо змінні оточення:
# 1. Забороняємо Python створювати файли кешу .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# 2. Дозволяємо вивід логів одразу в консоль (без буферизації)
ENV PYTHONUNBUFFERED 1

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /code

# Встановлюємо системні залежності для PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копіюємо файл залежностей і встановлюємо їх
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копіюємо весь наш код у контейнер
COPY . /code/