FROM python:3.4

RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple Flask uWSGI requests redis
WORKDIR /app
COPY app /app
COPY cmd.sh /
EXPOSE 9090 9191 5000
USER uwsgi
CMD ["/cmd.sh"]
