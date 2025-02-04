FROM python:3.13

WORKDIR /usr/backend

ENV PYTHONDONTWRITENYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY requirements.txt /usr/backend/

RUN python -m pip install gunicorn
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /usr/backend/
EXPOSE 8000