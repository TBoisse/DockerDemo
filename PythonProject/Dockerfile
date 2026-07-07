FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt requirements.txt
COPY src src
COPY main.py main.py

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]