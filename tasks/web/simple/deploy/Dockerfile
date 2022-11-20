FROM tiangolo/uwsgi-nginx-flask:python3.10

COPY app/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY keys /keys/

COPY app /app