# syntax=docker/dockerfile:1

FROM python:3.10.6-slim-buster

WORKDIR /bot

RUN echo  "deb http://mirrors.tuna.tsinghua.edu.cn/debian/ buster main contrib non-free" >/etc/apt/sources.list
RUN echo  "deb http://mirrors.tuna.tsinghua.edu.cn/debian/ buster-updates main contrib non-free" >>/etc/apt/sources.list
RUN echo  "deb http://mirrors.tuna.tsinghua.edu.cn/debian/ buster-backports main contrib non-free" >>/etc/apt/sources.list
RUN echo  "deb http://mirrors.tuna.tsinghua.edu.cn/debian-security buster/updates main contrib non-free" >>/etc/apt/sources.list
RUN apt-get update


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "main.py"]

