FROM python:3.9.6-slim-bullseye

WORKDIR /app

COPY app/requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY app .
COPY entry.sh .

CMD ./entry.sh