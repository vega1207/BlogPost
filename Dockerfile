FROM python:3.8-slim-buster

ENV CONTAINER_HOME=/home/ubuntu/project

ADD . $CONTAINER_HOME
WORKDIR $CONTAINER_HOME

RUN pip install -r  $CONTAINER_HOME/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple