# Базовий образ Python
FROM python:3.11-slim

# Змінні середовища для коректної роботи Python в контейнері
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Робоча директорія всередині контейнера
WORKDIR /app

# Копіюємо тільки файл з залежностями, щоб скористатися кешем Docker
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Копіюємо весь код у контейнер
COPY . .

RUN mkdir -p /app/staticfiles

# Збираємо статичні файли (якщо ви їх використовуєте)
#RUN python manage.py collectstatic --noinput

# Відкриваємо порт, на якому працюватиме Django
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
