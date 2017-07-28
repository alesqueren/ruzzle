FROM python:2.7-alpine

WORKDIR /app
ADD . .

ENTRYPOINT ["python", "ruzzle.py"]
