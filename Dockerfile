FROM tiangolo/uwsgi-nginx-flask:python3.8
ENV STATIC_URL /static
ENV STATIC_PATH /app/app/static
COPY ./app /app
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r /app/requirements.txt