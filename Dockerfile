FROM python:3.9-slim

LABEL description="Homesever image"

WORKDIR /usr/src/app

COPY . .

RUN apt-get update
RUN pip install pipenv
RUN pipenv install

ENTRYPOINT ["pipenv", "run", "python", "./main_dashboard.py"]