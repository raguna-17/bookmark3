FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 必要なOS依存
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && apt-get clean

# Python依存
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# プロジェクトコピー
COPY . .

# entrypoint 実行権限
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

CMD ["sh", "-c", "gunicorn project.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]

