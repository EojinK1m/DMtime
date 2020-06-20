FROM python:3.8.1

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN mkdir /var/log/uwsgi
RUN pip install uWsgi
RUN pip install -r requirements.txt

CMD ["uwsgi", "DMInside.ini"]
