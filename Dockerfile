FROM python:3.10

COPY ./pyproject.toml ./poetry.lock* todo/

WORKDIR todo/

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install 

RUN apt-get update && \
    apt-get install -y openssl

COPY todo/ todo/

# Create rsa certificates
RUN mkdir todo/core/certs && \
    openssl genrsa -out todo/core/certs/jwt-private.pem 2048 && \
    openssl rsa -in todo/core/certs/jwt-private.pem -pubout -out todo/core/certs/jwt-public.pem