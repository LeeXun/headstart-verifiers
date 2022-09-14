FROM python:3.9.12-buster

LABEL project=cns2022

WORKDIR /headstart

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./requirements.txt .
RUN pip install -r requirements.txt
