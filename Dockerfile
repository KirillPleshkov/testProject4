FROM python:3.12-slim
WORKDIR /usr/src/app

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#Обновляем pip
RUN pip install --upgrade pip

#Копируем пакеты отдельно для кэширования и тем самым ускорения сборки
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .