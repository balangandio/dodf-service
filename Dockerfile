FROM tiangolo/uwsgi-nginx-flask:python3.8
RUN apt-get update && apt-get install -y ca-certificates
ENV STATIC_URL /static
ENV STATIC_PATH /app/app/static
COPY ./app /app
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r /app/requirements.txt
RUN cat /app/requirements-nltk.txt | while read LINE; do python -m nltk.downloader $LINE; done