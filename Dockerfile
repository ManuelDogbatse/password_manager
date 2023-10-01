# Dockerfile, Image, Container
FROM python:3.11

WORKDIR /password-gen-app

COPY requirements.txt .

COPY docker.env .env

RUN pip install -r requirements.txt

COPY ./app ./app

CMD ["python3", "./app/password_manager.py"]