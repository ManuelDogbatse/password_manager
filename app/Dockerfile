# Dockerfile, Image, Container
FROM python:3.11

WORKDIR /ps-mg-app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./src ./src

CMD ["python3", "./src/password_manager.py"]