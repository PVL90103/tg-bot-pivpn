FROM python:3.12.8-slim

RUN apt-get update && apt-get install -y \
    qrencode \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
