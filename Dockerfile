FROM python:3.13-slim
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# если нужен веб-сервер — добавишь EXPOSE позже
# EXPOSE 5000

# по умолчанию запускаем CLI помощника
CMD ["./start.sh"]








