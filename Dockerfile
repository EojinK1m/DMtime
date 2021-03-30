FROM python:3.8.1


WORKDIR /app
ADD ./requirements.txt /app/
RUN pip install -r requirements.txt
RUN pip install uWsgi

RUN mkdir /var/log/uwsgi

ADD ./docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh


COPY . /app
RUN ln -s /usr/local/bin/docker-entrypoint.sh /


ENTRYPOINT ["docker-entrypoint.sh"]
