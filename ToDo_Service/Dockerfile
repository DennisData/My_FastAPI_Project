FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Объявляем том для хранения данных
VOLUME ["/app/data"]

# ENTRYPOINT ["tail", "-f", "/dev/null"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10001"]