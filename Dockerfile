FROM python:3.8.1

WORKDIR /app

COPY . /app

RUN pip install -r requitements.txt

CMD ["uwsgi", "DMInside.ini"]
