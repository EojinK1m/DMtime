FROM python:3.8.1

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN mkdir /var/log/uwsgi
RUN pip install uWsgi
RUN pip install -r requirements.txt


ENV DMTIME_DB_URI=${DMTIME_DB_USER}
ENV DMTIME_DB_USER=${DMTIME_DB_USER}
ENV DMTIME_DB_PW=${DMTIME_DB_PW}
ENV DMTIME_JWT_KEY=${DMTIME_JWT_KEY}
ENV DMTIME_SERVER_NAME=${DMTIME_SERVER_NAME}
ENV DMTIME_IMAGES_STORAGE=${DMTIME_IMAGES_STORAGE}



CMD ["uwsgi", "DMInside.ini"]
